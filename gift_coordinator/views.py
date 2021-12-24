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

def listPoolView(request):
    context = {}
    context['pools'] = GiftPool.objects.all()
    return render(request, "listPoolTemplate.html", context)

def createPoolView(request):
    if request.method == 'POST':
        form = CreatePoolForm(request.POST)

        # if all form values are valid
        if form.is_valid():

            # get some form data
            giftRecipName = form.cleaned_data.get('recipient_name').lower()
            newPoolVal = int(form.cleaned_data.get('amount'))

            # use that to get any existing GiftPool for this recipient
            pool = GiftPool.objects.filter(recipient_name=giftRecipName)
            
            if pool and pool.curr_val: # this is not the first person joining the gift pool
                newPoolVal = pool.curr_val + newPoolVal

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
            return redirect(reverse('createPoolUrl'))

    # show the view with the empty form
    context = {}
    context['form'] = CreatePoolForm()
    return render(request, "createPoolTemplate.html", context)
  