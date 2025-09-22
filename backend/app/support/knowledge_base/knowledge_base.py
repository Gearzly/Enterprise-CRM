from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import (
    Article, ArticleCreate, ArticleUpdate,
    ArticleCategory, ArticleCategoryCreate, ArticleCategoryUpdate,
    ArticleFeedback, ArticleFeedbackCreate
)
from .config import (
    get_article_categories, get_default_category, get_max_tags_per_article
)

router = APIRouter()

# In-memory storage for demo purposes
articles_db = []
categories_db = []
feedback_db = []

@router.get("/articles", response_model=List[Article])
def list_articles():
    """List all articles"""
    return articles_db

@router.get("/articles/{article_id}", response_model=Article)
def get_article(article_id: int):
    """Get a specific article by ID"""
    for article in articles_db:
        if article.id == article_id:
            return article
    raise HTTPException(status_code=404, detail="Article not found")

@router.post("/articles", response_model=Article)
def create_article(article: ArticleCreate):
    """Create a new article"""
    new_id = max([a.id for a in articles_db]) + 1 if articles_db else 1
    new_article = Article(
        id=new_id,
        created_at=datetime.now(),
        **article.dict()
    )
    articles_db.append(new_article)
    return new_article

@router.put("/articles/{article_id}", response_model=Article)
def update_article(article_id: int, article_update: ArticleUpdate):
    """Update an existing article"""
    for index, article in enumerate(articles_db):
        if article.id == article_id:
            updated_article = Article(
                id=article_id,
                created_at=article.created_at,
                updated_at=datetime.now(),
                **article_update.dict()
            )
            articles_db[index] = updated_article
            return updated_article
    raise HTTPException(status_code=404, detail="Article not found")

@router.delete("/articles/{article_id}")
def delete_article(article_id: int):
    """Delete an article"""
    for index, article in enumerate(articles_db):
        if article.id == article_id:
            del articles_db[index]
            return {"message": "Article deleted successfully"}
    raise HTTPException(status_code=404, detail="Article not found")

@router.get("/articles/search", response_model=List[Article])
def search_articles(query: str):
    """Search articles by title or content"""
    query = query.lower()
    results = []
    for article in articles_db:
        if (query in article.title.lower() or 
            query in article.content.lower() or
            any(query in tag.lower() for tag in article.tags)):
            results.append(article)
    return results

@router.post("/articles/{article_id}/publish")
def publish_article(article_id: int):
    """Publish an article"""
    for index, article in enumerate(articles_db):
        if article.id == article_id:
            articles_db[index].is_published = True
            articles_db[index].published_at = datetime.now()
            return {"message": "Article published successfully"}
    raise HTTPException(status_code=404, detail="Article not found")

@router.post("/articles/{article_id}/unpublish")
def unpublish_article(article_id: int):
    """Unpublish an article"""
    for index, article in enumerate(articles_db):
        if article.id == article_id:
            articles_db[index].is_published = False
            articles_db[index].published_at = None
            return {"message": "Article unpublished successfully"}
    raise HTTPException(status_code=404, detail="Article not found")

# Category endpoints
@router.get("/categories", response_model=List[ArticleCategory])
def list_categories():
    """List all categories"""
    return categories_db

@router.get("/categories/{category_id}", response_model=ArticleCategory)
def get_category(category_id: int):
    """Get a specific category by ID"""
    for category in categories_db:
        if category.id == category_id:
            return category
    raise HTTPException(status_code=404, detail="Category not found")

@router.post("/categories", response_model=ArticleCategory)
def create_category(category: ArticleCategoryCreate):
    """Create a new category"""
    new_id = max([c.id for c in categories_db]) + 1 if categories_db else 1
    new_category = ArticleCategory(
        id=new_id,
        created_at=datetime.now(),
        **category.dict()
    )
    categories_db.append(new_category)
    return new_category

@router.put("/categories/{category_id}", response_model=ArticleCategory)
def update_category(category_id: int, category_update: ArticleCategoryUpdate):
    """Update an existing category"""
    for index, category in enumerate(categories_db):
        if category.id == category_id:
            updated_category = ArticleCategory(
                id=category_id,
                created_at=category.created_at,
                updated_at=datetime.now(),
                **category_update.dict()
            )
            categories_db[index] = updated_category
            return updated_category
    raise HTTPException(status_code=404, detail="Category not found")

@router.delete("/categories/{category_id}")
def delete_category(category_id: int):
    """Delete a category"""
    for index, category in enumerate(categories_db):
        if category.id == category_id:
            del categories_db[index]
            return {"message": "Category deleted successfully"}
    raise HTTPException(status_code=404, detail="Category not found")

# Feedback endpoints
@router.get("/feedback", response_model=List[ArticleFeedback])
def list_feedback():
    """List all feedback"""
    return feedback_db

@router.post("/feedback", response_model=ArticleFeedback)
def create_feedback(feedback: ArticleFeedbackCreate):
    """Create new feedback"""
    new_id = max([f.id for f in feedback_db]) + 1 if feedback_db else 1
    new_feedback = ArticleFeedback(
        id=new_id,
        created_at=datetime.now(),
        **feedback.dict()
    )
    feedback_db.append(new_feedback)
    
    # Update article helpful counts
    for article in articles_db:
        if article.id == feedback.article_id:
            if feedback.is_helpful:
                article.helpful_count += 1
            else:
                article.not_helpful_count += 1
            break
    
    return new_feedback

@router.get("/articles/{article_id}/feedback", response_model=List[ArticleFeedback])
def get_article_feedback(article_id: int):
    """Get feedback for a specific article"""
    return [f for f in feedback_db if f.article_id == article_id]

# Configuration endpoints
@router.get("/config/categories", response_model=List[str])
def get_article_category_options():
    """Get available article category options"""
    return get_article_categories()