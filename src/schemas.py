from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)


class ContactBase(BaseModel):
    name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    e_mail: EmailStr
    phone_number: str = Field(max_length=20)
    born_date: str = Field(max_length=20)
    description: str = Field(max_length=150)


class NoteModel(NoteBase):
    tags: List[int]


class ContactModel(ContactBase):
    pass


class NoteUpdate(NoteModel):
    done: bool


class ContactUpdate(ContactModel):
    done: bool


class NoteStatusUpdate(BaseModel):
    done: bool


class ContactStatusUpdate(BaseModel):
    done: bool


class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    tags: List[TagResponse]

    class Config:
        from_attributes = True


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    # tags: List[TagResponse]

    class Config:
        from_attributes = True
