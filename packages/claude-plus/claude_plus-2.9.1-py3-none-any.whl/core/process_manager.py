#!/usr/bin/env python3
"""
Claude++ Process Manager
Advanced subprocess management with PTY handling, retries, and monitoring.
"""

import asyncio
import os
import pty
import select
import subprocess
import threading
import time
import signal
import json
import logging
from typing import Dict, List, Optional, Callable, Tuple, Any
from enum import Enum
from dataclasses import dataclass
import queue


class ProcessState(Enum):
    """Process state enumeration."""
    IDLE = "idle"
    STARTING = "starting" 
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    RETRY = "retry"


@dataclass
class ProcessConfig:
    """Configuration for managed process."""
    command: str
    args: List[str] = None
    timeout: float = 300.0
    max_retries: int = 3
    retry_delay: float = 2.0
    buffer_size: int = 8192
    use_pty: bool = True
    stream_json: bool = False
    auto_restart: bool = False


class ManagedProcess:
    """A managed subprocess with advanced control features."""
    
    def __init__(self, config: ProcessConfig, process_id: str = None):
        self.config = config
        self.process_id = process_id or f"proc_{int(time.time())}"
        self.logger = logging.getLogger(f'claude-plus.process.{self.process_id}')
        
        # Process state
        self.state = ProcessState.IDLE
        self.process = None
        self.master_fd = None
        self.slave_fd = None
        self.pid = None
        self.return_code = None
        
        # Monitoring
        self.start_time = None
        self.end_time = None
        self.retry_count = 0
        
        # Communication
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue() 
        self.reader_thread = None
        self.writer_thread = None
        
        # Callbacks
        self.output_callbacks = []
        self.state_callbacks = []
        self.error_callbacks = []
        
    def add_output_callback(self, callback: Callable[[str], None]):
        """Add callback for process output."""
        self.output_callbacks.append(callback)
        
    def add_state_callback(self, callback: Callable[[ProcessState, ProcessState], None]):
        """Add callback for state changes."""
        self.state_callbacks.append(callback)
        
    def add_error_callback(self, callback: Callable[[Exception], None]):
        """Add callback for errors."""
        self.error_callbacks.append(callback)
        
    def _set_state(self, new_state: ProcessState):
        """Set process state and notify callbacks."""
        old_state = self.state
        self.state = new_state
        
        self.logger.debug(f"State changed: {old_state.value} -> {new_state.value}")
        
        for callback in self.state_callbacks:
            try:
                callback(old_state, new_state)
            except Exception as e:
                self.logger.error(f"State callback error: {e}")
                
    def _notify_error(self, error: Exception):
        """Notify error callbacks."""
        for callback in self.error_callbacks:
            try:
                callback(error)
            except Exception as e:
                self.logger.error(f"Error callback error: {e}")
                
    def _notify_output(self, output: str):
        """Notify output callbacks."""
        for callback in self.output_callbacks:
            try:
                callback(output)
            except Exception as e:
                self.logger.error(f"Output callback error: {e}")
                
    async def start(self) -> bool:
        """Start the managed process."""
        if self.state != ProcessState.IDLE:
            self.logger.warning(f"Cannot start process in state: {self.state.value}")
            return False
            
        self._set_state(ProcessState.STARTING)
        self.start_time = time.time()
        
        try:
            await self._create_process()
            self._start_io_threads()
            self._set_state(ProcessState.RUNNING)
            
            self.logger.info(f"Process started successfully: PID {self.pid}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start process: {e}")
            self._set_state(ProcessState.ERROR)
            self._notify_error(e)
            return False
            
    async def _create_process(self):
        """Create the subprocess with PTY if configured."""
        full_args = [self.config.command]
        if self.config.args:
            full_args.extend(self.config.args)
            
        self.logger.info(f"Creating process: {' '.join(full_args)}")
        
        if self.config.use_pty:
            # Create PTY
            self.master_fd, self.slave_fd = pty.openpty()
            
            # Start process with PTY
            self.process = subprocess.Popen(
                full_args,
                stdin=self.slave_fd,
                stdout=self.slave_fd,
                stderr=self.slave_fd,
                close_fds=True,
                preexec_fn=os.setsid
            )
            
            # Close slave in parent
            os.close(self.slave_fd)
            self.slave_fd = None
            
        else:
            # Regular pipes
            self.process = subprocess.Popen(
                full_args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0
            )
            
        self.pid = self.process.pid
        
    def _start_io_threads(self):
        """Start I/O handling threads."""
        self.reader_thread = threading.Thread(
            target=self._reader_loop,
            name=f"reader-{self.process_id}",
            daemon=True
        )
        self.reader_thread.start()
        
        self.writer_thread = threading.Thread(
            target=self._writer_loop,
            name=f"writer-{self.process_id}",
            daemon=True
        )
        self.writer_thread.start()
        
    def _reader_loop(self):
        """Read output from process in background thread."""
        try:
            if self.config.use_pty:
                self._read_from_pty()
            else:
                self._read_from_pipes()
        except Exception as e:
            self.logger.error(f"Reader thread error: {e}")
            self._notify_error(e)
            
    def _read_from_pty(self):
        """Read from PTY master."""
        while self.state == ProcessState.RUNNING:
            try:
                # Use select to avoid blocking
                ready, _, _ = select.select([self.master_fd], [], [], 0.1)
                
                if ready:
                    data = os.read(self.master_fd, self.config.buffer_size)
                    if not data:
                        break
                        
                    text = data.decode('utf-8', errors='ignore')
                    self._process_output(text)
                    
            except OSError:
                # PTY closed
                break
            except Exception as e:
                self.logger.error(f"PTY read error: {e}")
                break
                
    def _read_from_pipes(self):
        """Read from regular pipes."""
        while self.state == ProcessState.RUNNING and self.process:
            try:
                line = self.process.stdout.readline()
                if not line:
                    break
                    
                self._process_output(line)
                
            except Exception as e:
                self.logger.error(f"Pipe read error: {e}")
                break
                
    def _process_output(self, text: str):
        """Process output text and handle JSON streaming if configured."""
        if self.config.stream_json:
            # Try to parse as JSON lines
            for line in text.strip().split('\n'):
                if line.strip():
                    try:
                        json_data = json.loads(line)
                        self._handle_json_output(json_data)
                    except json.JSONDecodeError:
                        # Regular text output
                        self._handle_text_output(line)
        else:
            self._handle_text_output(text)
            
    def _handle_json_output(self, json_data: Dict[str, Any]):
        """Handle JSON formatted output."""
        # Add to queue for processing
        self.output_queue.put(('json', json_data))
        
        # Notify callbacks with formatted text
        text = json.dumps(json_data, indent=2)
        self._notify_output(text)
        
    def _handle_text_output(self, text: str):
        """Handle regular text output."""
        # Add to queue
        self.output_queue.put(('text', text))
        
        # Notify callbacks
        self._notify_output(text)
        
    def _writer_loop(self):
        """Write input to process in background thread."""
        try:
            while self.state == ProcessState.RUNNING:
                try:
                    # Get input from queue with timeout
                    input_data = self.input_queue.get(timeout=0.1)
                    
                    if self.config.use_pty:
                        os.write(self.master_fd, input_data.encode('utf-8'))
                    else:
                        self.process.stdin.write(input_data)
                        self.process.stdin.flush()
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    self.logger.error(f"Write error: {e}")
                    break
                    
        except Exception as e:
            self.logger.error(f"Writer thread error: {e}")
            
    def send_input(self, data: str):
        """Send input to the process."""
        if self.state != ProcessState.RUNNING:
            self.logger.warning(f"Cannot send input in state: {self.state.value}")
            return False
            
        try:
            self.input_queue.put(data)
            return True
        except Exception as e:
            self.logger.error(f"Failed to queue input: {e}")
            return False
            
    def get_output(self, timeout: float = None) -> Optional[Tuple[str, Any]]:
        """Get output from the process queue."""
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return None
            
    async def stop(self, graceful: bool = True, timeout: float = 5.0) -> bool:
        """Stop the managed process."""
        if self.state not in [ProcessState.RUNNING, ProcessState.STARTING]:
            return True
            
        self._set_state(ProcessState.STOPPING)
        
        try:
            if graceful and self.process:
                # Try graceful shutdown first
                self.process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.return_code = self.process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    # Force kill if timeout
                    self.logger.warning("Graceful shutdown timeout, force killing")
                    self.process.kill()
                    self.return_code = self.process.wait()
            else:
                # Force kill immediately
                if self.process:
                    self.process.kill()
                    self.return_code = self.process.wait()
                    
            # Cleanup resources
            await self._cleanup()
            
            self.end_time = time.time()
            self._set_state(ProcessState.STOPPED)
            
            self.logger.info(f"Process stopped with code: {self.return_code}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping process: {e}")
            self._set_state(ProcessState.ERROR)
            self._notify_error(e)
            return False
            
    async def _cleanup(self):
        """Clean up process resources."""
        # Close PTY
        if self.master_fd:
            try:
                os.close(self.master_fd)
            except OSError:
                pass
            self.master_fd = None
            
        # Wait for threads to finish
        if self.reader_thread and self.reader_thread.is_alive():
            self.reader_thread.join(timeout=1.0)
            
        if self.writer_thread and self.writer_thread.is_alive():
            self.writer_thread.join(timeout=1.0)
            
    async def restart(self) -> bool:
        """Restart the process."""
        self.logger.info("Restarting process")
        
        # Stop current process
        await self.stop()
        
        # Increment retry count
        self.retry_count += 1
        
        if self.retry_count > self.config.max_retries:
            self.logger.error(f"Max retries ({self.config.max_retries}) exceeded")
            return False
            
        # Wait before restart
        await asyncio.sleep(self.config.retry_delay)
        
        # Reset state and start
        self._set_state(ProcessState.IDLE)
        return await self.start()
        
    def get_status(self) -> Dict[str, Any]:
        """Get process status information."""
        runtime = None
        if self.start_time:
            end = self.end_time or time.time()
            runtime = end - self.start_time
            
        return {
            'process_id': self.process_id,
            'state': self.state.value,
            'pid': self.pid,
            'return_code': self.return_code,
            'retry_count': self.retry_count,
            'runtime': runtime,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'command': f"{self.config.command} {' '.join(self.config.args or [])}"
        }


class ProcessManager:
    """Manages multiple processes with coordination."""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.process_manager')
        self.processes: Dict[str, ManagedProcess] = {}
        self.running = False
        
    def create_process(self, config: ProcessConfig, process_id: str = None) -> str:
        """Create a new managed process."""
        process = ManagedProcess(config, process_id)
        process_id = process.process_id
        
        self.processes[process_id] = process
        self.logger.info(f"Created process: {process_id}")
        
        return process_id
        
    def get_process(self, process_id: str) -> Optional[ManagedProcess]:
        """Get a managed process by ID."""
        return self.processes.get(process_id)
        
    async def start_process(self, process_id: str) -> bool:
        """Start a managed process."""
        process = self.get_process(process_id)
        if not process:
            self.logger.error(f"Process not found: {process_id}")
            return False
            
        return await process.start()
        
    async def stop_process(self, process_id: str, graceful: bool = True) -> bool:
        """Stop a managed process."""
        process = self.get_process(process_id)
        if not process:
            self.logger.error(f"Process not found: {process_id}")
            return False
            
        return await process.stop(graceful)
        
    async def restart_process(self, process_id: str) -> bool:
        """Restart a managed process."""
        process = self.get_process(process_id)
        if not process:
            self.logger.error(f"Process not found: {process_id}")
            return False
            
        return await process.restart()
        
    def remove_process(self, process_id: str) -> bool:
        """Remove a managed process."""
        if process_id in self.processes:
            process = self.processes[process_id]
            if process.state == ProcessState.RUNNING:
                self.logger.warning(f"Removing running process: {process_id}")
                
            del self.processes[process_id]
            return True
        return False
        
    def list_processes(self) -> List[Dict[str, Any]]:
        """List all managed processes with their status."""
        return [process.get_status() for process in self.processes.values()]
        
    async def stop_all(self, graceful: bool = True):
        """Stop all managed processes."""
        self.logger.info("Stopping all processes")
        
        tasks = []
        for process in self.processes.values():
            if process.state == ProcessState.RUNNING:
                tasks.append(process.stop(graceful))
                
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
        self.logger.info("All processes stopped")