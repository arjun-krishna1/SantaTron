from django.shortcuts import (
    render,
    redirect,
    reverse,
)

from .models import (
    GiftPool,
    Contributor,
)

from .forms import CreatePoolForm

def createPoolView(request):
    if request.method == 'POST':
        form = CreatePoolForm(request.POST)
        if form.is_valid():

            giftRecipName = form.cleaned_data.get('recipient_name').lower()
            
            pool = GiftPool.objects.filter(recipient_name=giftRecipName)
            
            newPoolVal = int(form.cleaned_data.get('amount'))
            
            if pool and pool.curr_val: # this is not the first person joining the gift pool
                newPoolVal = pool.curr_val + newPoolVal

            else:
                pool = GiftPool(
                    recipient_name = giftRecipName,
                    curr_val = newPoolVal,
                    )

            # save this GiftPool
            pool.save()

            # create this contributor entry
            contributor = Contributor(
                name = form.cleaned_data.get('contributor_name'),
                amount_contributed = form.cleaned_data.get('amount'),
                gift_pool = pool,
                keyword1 = form.cleaned_data.get('keyword1'),
                keyword2 = form.cleaned_data.get('keyword2'),
                keyword3 = form.cleaned_data.get('keyword3')
            )

            contributor.save()
            return redirect(reverse('createPoolUrl'))


    context = {}
    context['form'] = CreatePoolForm()
    return render(request, "createPoolTemplate.html", context)
  