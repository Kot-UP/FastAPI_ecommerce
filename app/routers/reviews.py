from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user
from app.backend.db_depends import get_db
from app.models import *
from app.schemas import CreateReview, CreateRating, CreateProduct
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get('/all_reviews')
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active==True))

    if reviews is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no comments"
        )

    return reviews.all()

@router.get('/products_reviews')
async def products_reviews(db: Annotated[AsyncSession,Depends(get_db)], product_slug: str):
    product = await db.scalars(select(Product).where(Product.slug == product_slug))

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product"
        )

    product_comment = await db.scalars(select(Review).where(Review.comment, Review.rating_id.grade, Review.product_id == product.id))

    return product_comment.all()

@router.post('/add_review')
async def add_review(db: Annotated[AsyncSession, Depends(get_db)],
                     create_review: CreateReview,
                     create_rating: CreateRating,
                     create_product: CreateProduct,
                     slug_product: str,
                     get_user: Annotated[dict, Depends(get_current_user)]):

    if get_user.get('is_customer'):
        review_com = await db.execude(insert(Review).values(product_id=create_review.product_id,
                                               commen=create_review.commen))
        await db.execude(update(Product).where(Product.slug == slug_product).values(rating=create_product.rating))
        await db.commit()

        return {
                'status_code': status.HTTP_200_OK,
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method')

@router.delete('/delete')
async def delete_reviews(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)],
                         id_product: int):
    if get_user.get('is_admin'):
        db.execude(update(Review).where(Review.product_id == id_product).values(is_active=False))
        db.execude(update(Rating).where(Rating.product_id == id_product).values(is_active=False))
        await db.commit()
        return {'status_code': status.HTTP_200_OK}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )