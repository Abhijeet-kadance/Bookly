from fastapi import APIRouter, status, Depends, Query, Cookie
from typing import List, Annotated
from fastapi.exceptions import HTTPException
from src.books.schemas import Book, BookUpdateModel,BookCreateModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from pydantic import BaseModel
from src.auth.dependencies import AccessTokenBearer

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()

# fake_items_db = [{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None    

# @book_router.get("/items")
# async def read_items(
#     q:Annotated[str | None ,Cookie()] = None,
# ) -> dict:
#     results = {"items":[{"item_id":"Foo"},{"item_id":"Fax"}]}
#     if q:
#         results.update({"q":q})
#     return results


# @book_router.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax":price_with_tax})
#     return item_dict
    
# @book_router.get('/items')
# async def get_items(skip: int = 0, limit: int = 1):
#     return fake_items_db[skip:skip + limit]

# @book_router.get('/items/{item_id}')
# async def read_item(item_id:str, q:str | None = None, short: bool = False):
#     item = {"item_id":item_id}
#     if q:
#         item.update({"q":q})
#     if not short:
#         item.update(
#             {"description":"This is an amazing item"}
#         )
#     return item 

@book_router.get("/",response_model=List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session),user_details=Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/",status_code=status.HTTP_201_CREATED,response_model=Book)
async def create_a_book(book_data:BookCreateModel, session:AsyncSession = Depends(get_session)) -> dict:
    new_book = await book_service.create_book(book_data,session)
    return new_book

@book_router.get('/{book_uid}',response_model=Book)
async def get_book(book_uid:str, session:AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid,session)
    
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not Found !")


@book_router.patch('/{book_uid}', response_model=Book)
async def update_book(book_uid: str,book_update_data:BookUpdateModel,session:AsyncSession = Depends(get_session)) -> dict:
    
    updated_book = await book_service.update_book(book_uid,book_update_data,session)
    
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found!")

@book_router.delete('/{book_uid}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid:str,session:AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found !")
            
        
