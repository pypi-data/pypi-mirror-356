"""Utilitários para acompanhamento de progresso"""

from abc import ABC, abstractmethod
from typing import Optional
import sys
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.console import Console


class ProgressCallback(ABC):
    """Interface para callbacks de progresso"""
    
    @abstractmethod
    def update(self, current: int, total: int, message: Optional[str] = None):
        """Atualiza o progresso"""
        pass
    
    @abstractmethod
    def finish(self):
        """Finaliza o progresso"""
        pass


class ConsoleProgress(ProgressCallback):
    """Progresso no console usando Rich"""
    
    def __init__(self, description: str = "Uploading"):
        self.console = Console()
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=self.console
        )
        self.task = None
        self.description = description
        self._started = False
    
    def start(self, total: int):
        """Inicia o progresso"""
        if not self._started:
            self.progress.start()
            self._started = True
        self.task = self.progress.add_task(self.description, total=total)
    
    def update(self, current: int, total: int, message: Optional[str] = None):
        """Atualiza o progresso"""
        if not self._started:
            self.start(total)
        
        if self.task is not None:
            self.progress.update(self.task, completed=current)
            if message:
                self.progress.update(self.task, description=message)
    
    def finish(self):
        """Finaliza o progresso"""
        if self._started:
            self.progress.stop()
            self._started = False


class SimpleProgress(ProgressCallback):
    """Progresso simples no console"""
    
    def __init__(self, description: str = "Progress"):
        self.description = description
        self.last_percent = -1
    
    def update(self, current: int, total: int, message: Optional[str] = None):
        """Atualiza o progresso"""
        if total == 0:
            return
        
        percent = int((current / total) * 100)
        
        # Só atualiza se mudou a porcentagem
        if percent != self.last_percent:
            self.last_percent = percent
            bar_length = 30
            filled_length = int(bar_length * current // total)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            msg = message or self.description
            sys.stdout.write(f'\r{msg}: |{bar}| {percent}%')
            sys.stdout.flush()
    
    def finish(self):
        """Finaliza o progresso"""
        sys.stdout.write('\n')
        sys.stdout.flush()