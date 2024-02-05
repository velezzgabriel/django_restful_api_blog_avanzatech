# ReadME.md

# DJANGO PROJECT ETAPA 7

## Objective:

The objective of this lab is to create a robust blogging platform using Django that includes user authentication, permissions, and a RESTful API. Users will be able to create, read, update, and delete their own blog posts, as well as read, like, and comment on other users' posts. Additionally, the lab will include admin functionality with full permissions on all posts.

## **Virtual Environment Setup**

This guide will help you set up a virtual environment for the blog project using pipenv. Pipenv is a tool that provides all necessary package management functionalities for Python projects.

### **1. Install pipenv**

If you haven't installed pipenv yet, you can do so using pip, the Python package installer:

```bash
pip install pipenv
```

### **2. Clone the Repository**

Clone the blog project repository from GitHub:

```bash
git clone https://github.com/velezzgabriel/etapa7.git
```

### **3. Navigate to the Project Directory**

Change your current directory to the root directory of the cloned project:

```bash
cd etapa7
```

### **4. Install Dependencies**

Pipenv uses the Pipfile in your project to manage dependencies. To install all dependencies specified in the Pipfile, run:

```bash
pipenv install
```

This command will create a virtual environment for the project and install all required dependencies inside it.

### **5. Activate the Virtual Environment**

To activate the virtual environment created by pipenv, run:

```bash
pipenv shell
```

This command will activate the virtual environment, and you'll see the environment name in your shell prompt.

### **6. Running the Project**

Once the virtual environment is activated, you can run the Django project using manage.py commands:

```bash
python manage.py runserver
```

This command will start the Django development server, and you can access your blog project at the specified address ( usually http://127.0.0.1:8000/).

### **7. Deactivate the Virtual Environment**

To deactivate the virtual environment and return to your system's global Python environment, simply type:

```bash
exit
```

This will deactivate the virtual environment and return you to your previous shell environment.

## **Apps Overview**

1. **user**: Manages user authentication. User authentication using Django's built-in authentication system has been implemented.
2. **teams**: It is basically a model to store the teams that the users belong to. Each user is a member of exactly 1 team. Admin users can read/edit any post in the website and are not restricted by the permissions system
3. **posts**: Handles creation, retrieval, update, and deletion of posts. Permissions in posts determine the visibility and edition ability for the users. 
4. **likes**: Manages likes on posts, their creation and deletion. Non auth users cannot like a post regardless of the post permission.
5. **comments**: Handles comments on posts, their creation and deletion. Non auth users cannot comment a post regardless of the post permission.

## Admin Panel

Django's admin panel configured to manage blog posts and user accounts. Site Admins  able to perform CRUD operations on all posts. Note that a “site admin” is different than the admin user role.

## Permissions

The permissions system assigns each blog post access controls for reading and writing. The 4 options are:

1. **Public**: anyone can access the post
2. **Authenticated**: any authenticated user can access the post
3. **Team**: Any user on the same team as the post author can access the post
4. **Author**: Only the author can access the post

The access control for reading and editing are independent of each other

# Main Project:  avanzatech_blog

urls.py

```python
urlpatterns = [
    # swagger documentation
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc',
                                        cache_timeout=0), name='schema-redoc'),

    # USER app
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),

    # POSTS app
    path('blog/', include('posts.urls')),
    path('post/', include('posts.urls')),

    # COMMENTS app
    path('comments/', include('comments.urls')),

    # LIKES app
    path('likes/', include('likes.urls')),

]
```

# **Views and URL patterns for each of the apps:**

## **User app:**

### **user Views:**

- **login_view**: Handles user login functionality.
- **logout_view**: Handles user logout functionality.

### user UR**L patterns:**

```python
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

## **Posts app:**

### **posts Views:**

- **PostCreateOrList**: Allows creation and listing of posts.
    - **Payload must contain for post creation:**
    
    ```python
    title
    post_content
    permission (CHOICES= 'public','authenticated','team','author')
    ```
    
- **PostRetrieveUpdateDestroy**: Allows retrieval, update, and deletion of posts.
    - **Kwargs must contain for post retrieve, update and destroy:**
    
    ```python
    pk (post primary key)
    ```
    
    - **Payload must contain for post update at least one of the following:**
    
    ```python
    title
    post_content
    permission (CHOICES= 'public','authenticated','team','author')
    ```
    

### posts UR**L patterns:**

```python
urlpatterns = [
    path('create/', LikeCreate.as_view(), name='likesCreate'),
    path('', LikeList.as_view(), name='likesList'),
    path('<int:author>/<int:post_id>/',
         LikeDestroy.as_view(), name='likesDestroy'),
]
```

## **Likes app:**

### **likes Views:**

- **LikeCreate**: Creation of a like in a post.
    - **Payload must contain for like creation:**
    
    ```python
    post_id (post foreign key)
    author (user foreign key)
    ```
    
- **LikeList**: Lists likes on posts.
    - LikeList view does not require either payload or kwargs.
    - It is possible to filter  likes by post and user.
- **LikeDestroy**: Deletes a like on a post.
    - **Kwargs needed for like destroy:**
    
    ```python
    pk (like primary key)
    ```
    

### likes UR**L patterns:**

```python
urlpatterns = [
    path('create/', LikeCreate.as_view(), name='likesCreate'),
    path('', LikeList.as_view(), name='likesList'),
    path('<int:author>/<int:post_id>/',
         LikeDestroy.as_view(), name='likesDestroy'),
]
```

### 

## **Comments app:**

### **comment Views:**

- **CommentCreate**: Creation of a comment in a post.
    - **Payload must contain for comment creation:**
    
    ```python
    post_id (post foreign key)
    author (user foreign key)
    comment_content
    ```
    
- **CommentList**: Lists comments on posts.
    - CommentList view does not require either payload or kwargs.
    - It is possible to filter  likes by post and user.
- **CommentDestroy**: Deletes a comment on a post.
    - **Kwargs needed for like destroy:**
    
    ```python
    pk (comment primary key)
    ```
    

### comment UR**L patterns:**