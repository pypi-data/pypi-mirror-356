import abc

from pydantic import BaseModel


class UserState(BaseModel):
    task_id: str | None
    context_id: str | None


class UserStateStore(abc.ABC):
    @abc.abstractmethod
    async def get(self, user_id: str) -> UserState:
        pass

    @abc.abstractmethod
    async def set(self, user_id: str, state: UserState) -> None:
        pass


class InMemoryUserStateStore(UserStateStore):
    def __init__(self) -> None:
        self.store: dict[str, UserState] = {}

    async def get(self, user_id: str) -> UserState:
        return self.store.get(user_id) or UserState(task_id=None, context_id=None)

    async def set(self, user_id: str, state: UserState) -> None:
        self.store[user_id] = state
