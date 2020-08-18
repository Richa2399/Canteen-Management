from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from app.models import *
User=get_user_model()
from app.models import CanteenProfile
class SpeciesListFilter(admin.SimpleListFilter):

   
    title = 'Canteen Wise'
    parameter_name = 'Canteen Wise'

    default_value = None

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_of_canteen = []
        queryset = User.objects.filter(is_restaurant=True)
        
        for canteen in queryset:
            list_of_canteen.append(
                (str(canteen.id), canteen.first_name)
            )
        return sorted(list_of_canteen, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        #print(self.value())
        if self.value():
            #return queryset
            return Menu.objects.filter(canteen=User.objects.get(id=self.value()))
        return queryset
    
class IngredientInline(admin.TabularInline):
    model = Ingredients
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_filter=[SpeciesListFilter]
    list_display=['canteen','food_categoary','food_name','description','food_image','price','uploaded_at','rating']

    inlines = [
        IngredientInline

    ]



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email'] 
    list_filter = ('is_student', 'is_staff','is_restaurant') 
    fields = [('first_name', 'last_name'),('username',),('email',),('phone'),('profile',)]



class OrderInline(admin.TabularInline):
    model = Myorder
    extra = 0

    
@admin.register(Orders)
class MyOrderAdmin(admin.ModelAdmin):
    list_display = ['ordered_by','ordered_to','time','payment_status','transaction_id','uploaded_at','status','ordered_at','total_price'] 
    list_filter = ('status', 'payment_status') 
    inlines = [
        OrderInline,
    ]
    date_hierarchy = 'uploaded_at'
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.site_title = "Food Funday"
admin.site.site_header = "Food Funday" 
admin.site.unregister(Group)

  

class CanteenListFilter(admin.SimpleListFilter):

   
    title = 'Canteen Wise'
    parameter_name = 'Canteen Wise'

    default_value = None

    def lookups(self, request, model_admin):
       
        list_of_canteen = []
        queryset = User.objects.filter(is_restaurant=True)
        
        for canteen in queryset:
            list_of_canteen.append(
                (str(canteen.id), canteen.first_name)
            )
        return sorted(list_of_canteen, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        #print(self.value())
        if self.value():
            #return queryset
            return Category.objects.filter(canteen_name=User.objects.get(id=self.value()))
        return queryset

    
class MenuInline(admin.TabularInline):
    model = Menu
    extra = 0
    exclude=('canteen',)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['category_name','canteen_name']
    list_filter=[CanteenListFilter]
    inlines = [
        MenuInline,
    ]
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(CanteenProfile)
class CanteenAdmin(admin.ModelAdmin):
    list_display=('canteen','c','status','canteen_rating')
    list_filter=['status']


    def c(self, instance):
        return instance.canteen.phone
    c.short_description = 'foo'