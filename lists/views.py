from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item,List

# Create your views here.
def home_page(request):
    return render(request,'home.html')
    # else:
    #     new_item_text=''
    # item=Item()
    # item.text=request.POST.get('item_text','')
    # item.save()
    # return render(request,'home.html',{'new_item_text':new_item_text,})
    # return HttpResponse('<html><title>To-Do lists</title></html>')

# def test_can_save_a_POST_request(self):
#     response=self.client.post('/',data={'item_text':'A new list item'})

#     self.assertEqual(Item.objects.count(),1)
#     new_item=Item.objects.first()
#     self.assertEqual(new_item.text,'A new list item')
#     self.assertTemplateUsed(response,'home.html')

def view_list(request,list_id):
    list_=List.objects.get(id=list_id)
    return render(request,'list.html',{'list':list_})

def new_list(request):
    list_=List.objects.create()
    Item.objects.create(text=request.POST['item_text'],list=list_)
    return redirect(f'/lists/{list_.id}/')
def add_item(request,list_id):
    list_=List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'],list=list_)
    return redirect(f'/lists/{list_.id}/')
    