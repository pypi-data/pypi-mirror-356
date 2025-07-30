from typing import List, Optional

from .lib import Base


class Folders(Base):
    def list(
            self,
            folder_types: Optional[tuple[str]] = ('a', 'c', 'd', 'g', 'h'),
    ):
        return self._make_request(
            'folders.list',
            params={'types[]': list(folder_types)},
            method='get',
        )

    def create(self, name: str, rooms: List[str]):
        return self._make_request('folders.create', payload={
            'folderName': name,
            'rooms': rooms,
        })

    def add_room(self, folder_id: str, rooms: List[str]):
        return self._make_request('folders.addRoom', payload={
            'folderId': folder_id,
            'roomIds': rooms,
        })

    def remove_room(self, folder_id: str, rooms: List[str]):
        return self._make_request('folders.removeRoom', payload={
            'folderId': folder_id,
            'roomIds': rooms,
        })

    def pinned_room(self, folder_id: str, rooms: List[str]):
        return self._make_request('folders.savePinnedRooms', payload={
            'folderId': folder_id,
            'pinnedRoomIds': rooms,
        })

    def update(self, folder_id: str, name: str):
        return self._make_request('folders.update', payload={
            'folderId': folder_id,
            'folderName': name,
        })

    def remove(self, folder_id: str):
        return self._make_request(
            'folders.remove', payload={'folderId': folder_id},
        )
