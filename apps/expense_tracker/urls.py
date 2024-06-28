from django.urls import path

app_name = 'expense_tracker'


from apps.expense_tracker.View import category, budget, expense

urlpatterns = [
    ## For Category
    path('category-create/', category.CategoryCreateView.as_view(), name='category_create'),
    path('category-list/', category.CategoryListView.as_view(), name='category_list'),
    path('category-update/<int:pk>/', category.CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/', category.CategoryDeleteView.as_view(), name='category_delete'),


    ## For Budget
    path('budget-create/', budget.BudgetCreateView.as_view(), name='budget_create'),
    path('budget-list/', budget.BudgetListView.as_view(), name='budget_list'),
    path('budget-update/<int:pk>/', budget.BudgetUpdateView.as_view(), name='budget_update'),
    path('budget-delete/', budget.BudgetDeleteView.as_view(), name='budget_delete'),

]