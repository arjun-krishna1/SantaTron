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
from gift_coordinator.clustering import update_gift_product

def listPoolView(request):
    context = {}
    context['pools'] = GiftPool.objects.all()
    return render(request, "listPoolTemplate.html", context)

def createPoolView(request, recipient_name=''):
    if request.method == 'POST':
        form = CreatePoolForm(request.POST)

        # if all form values are valid
        if form.is_valid():

            # get some form data
            giftRecipName = form.cleaned_data.get('recipient_name').lower()
            newPoolVal = int(form.cleaned_data.get('amount'))

            # use that to get any existing GiftPool for this recipient
            pool = GiftPool.objects.filter(recipient_name=giftRecipName)
            if len(pool) > 0:
                pool = pool[0]
            if pool and pool.curr_val: # this is not the first person joining the gift pool
                newPoolVal = pool.curr_val + newPoolVal
                pool.curr_val = newPoolVal

            else: # make a new gift pool for this recipient
                pool = GiftPool(
                    recipient_name = giftRecipName,
                    curr_val = newPoolVal,
                    )

            # save this GiftPool
            pool.save()

            # create this contributor entry using information from the form
            # and the recipient's gift pool
            contributor = Contributor(
                name = form.cleaned_data.get('contributor_name'),
                amount_contributed = form.cleaned_data.get('amount'),
                gift_pool = pool,
                keyword1 = form.cleaned_data.get('keyword1'),
                keyword2 = form.cleaned_data.get('keyword2'),
                keyword3 = form.cleaned_data.get('keyword3')
            )

            # save this contributor
            contributor.save()

            # TODO redirect them to the list pools view
            return redirect(reverse('listPoolUrl'))

    # show the view with the empty form
    context = {}

    context['recipient_name'] = recipient_name
    if len(recipient_name):
        context['form'] = CreatePoolForm({'recipient_name': recipient_name})

    else: 
        context['form'] = CreatePoolForm()

    return render(request, "createPoolTemplate.html", context)

def chooseGiftView(request, recipient_name):
    current_pool = GiftPool.objects.get(recipient_name=recipient_name)
    pool_id = current_pool.pk
    url = update_gift_product(pool_id)
    current_pool.url = url
    current_pool.save()
    context = {"gift_url": url}
    return render(request, 'chooseGiftTemplate.html', context)
  