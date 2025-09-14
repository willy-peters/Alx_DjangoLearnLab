# Permissions & Groups Setup

## Custom Permissions
Defined in the Book model:

- `can_view`: Allows viewing books
- `can_create`: Allows creating books
- `can_edit`: Allows editing books
- `can_delete`: Allows deleting books

## User Groups
- **Viewers** → can_view
- **Editors** → can_view, can_create, can_edit
- **Admins** → all permissions

## Enforcement in Views
Views are protected using `@permission_required`:

```python
@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    ...
