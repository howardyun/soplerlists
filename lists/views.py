from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method=='POST':
        new_item_text=request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')
    items=Item.objects.all()
    return render(request,'home.html',{'items':items})
    # else:
    #     new_item_text=''
    # item=Item()
    # item.text=request.POST.get('item_text','')
    # item.save()
    # return render(request,'home.html',{'new_item_text':new_item_text,})
    # return HttpResponse('<html><title>To-Do lists</title></html>')

def test_can_save_a_POST_request(self):
    response=self.client.post('/',data={'item_text':'A new list item'})

    self.assertEqual(Item.objects.count(),1)
    new_item=Item.objects.first()
    self.assertEqual(new_item.text,'A new list item')
    self.assertTemplateUsed(response,'home.html')
