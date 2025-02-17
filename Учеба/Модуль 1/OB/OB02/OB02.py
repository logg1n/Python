from typing import List, Optional


class User:
    def __init__(self, user_id: int, name: str, access_level: str = "user"):
        self.__id = user_id
        self._name = name
        self.__access_level = access_level

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self._name

    @property
    def access_level(self) -> str:
        return self.__access_level

    def __repr__(self) -> str:
        return f"User(id={self.__id}, name={self._name}, access_level={self.__access_level})"


class Admin(User):
    def __init__(self, user_id: int, name: str):
        super().__init__(user_id, name, access_level="admin")
        self._users: List[User] = []

    def add_user(self, user: User) -> None:
        if user not in self._users:
            self._users.append(user)
            print(f"Пользователь {user.name} добавлен.")
        else:
            print(f"Пользователь {user.name} уже существует.")

    def remove_user(self, user_id: int) -> User:
        for user in self._users:
            if user.id == user_id:
                self._users.remove(user)
                print(f"Пользователь {user.name} удален.")
                return user
        print(f"Пользователь с ID {user_id} не найден.")
        return None


if __name__ == "__main__":
    admin = Admin(user_id=1, name="AdminUser")

    user1 = User(user_id=2, name="Alice")
    user2 = User(user_id=3, name="Bob")


# User(id=1, name=AdminUser, access_level=admin)
# Пользователь Alice добавлен.
# Пользователь Bob добавлен.
# Пользователь Alice удален.
# Удален: User(id=2, name=Alice)
