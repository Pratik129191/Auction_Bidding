from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.html import format_html

from core.forms import CustomRegisterForm
from .models import Auction, AuctionBid, Bid, Product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Avg, Count, Max, IntegerField, Value
from core.models import User


def home(request):
    return render(request, 'home.html')


@login_required
def auctions(request):
    all_auctions = Auction.objects.all()
    paginator = Paginator(all_auctions, 18)
    page = request.GET.get('page')
    auctions = paginator.get_page(page)
    context = {
        'auctions': auctions,
    }
    return render(request, 'auctions.html', context)


@login_required
def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    if request.method == 'POST':
        submitted_amount = request.POST.get('amount')

        bid_queryset = Bid.objects.filter(user=request.user, status=False)
        if bid_queryset.exists():
            bid = bid_queryset[0]
        else:
            bid = Bid.objects.create(user=request.user, auction_id=auction.id)

        auction_bid = AuctionBid.objects.create(
            user=request.user,
            auction=auction,
            bid=bid,
            offer=submitted_amount,
        )
        bid.offer = auction_bid.offer
        bid.save()

        largest = AuctionBid.objects.filter(auction_id=auction).values('offer').latest('offer')
        x = AuctionBid.objects.filter(offer__exact=submitted_amount, user=request.user).values('offer').latest('offer')
        print(largest)
        print(x)
        if largest == x:
            x = Auction.objects.get(pk=auction.id)
            print(x)
            x.winner_id = request.user.id
            x.save()
        # x = Auction.objects.filter(pk=auction).order_by('-auctionbid__offer').values('winner_id')[0]
        # largest = AuctionBid.objects.filter()
        return redirect('system:confirm-bids')

    context = {
        'auction': auction,
    }
    return render(request, 'auction_detail.html', context)


@login_required
def bid_summary(request):
    bids = AuctionBid.objects.filter(user=request.user)
    context = {
        'bids': bids,
    }
    return render(request, 'bid-summary.html', context)


@login_required
def confirm_bids(request):
    auction_bid_queryset = AuctionBid.objects.filter(user=request.user, confirmed=False)
    if auction_bid_queryset.exists():
        bid_id = auction_bid_queryset[0].bid.id
        for bid in auction_bid_queryset:
            bid.confirmed = True
            bid.save()

        bid = Bid.objects.filter(id=bid_id)[0]
        bid.status = True
        bid.offer = auction_bid_queryset[0].bid.offer
        bid.save()

    return redirect('system:bid-summary')


def about(request):
    return render(request, 'about.html')


@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_users = User.objects.count()
    total_auctions = Auction.objects.count()
    total_offers = AuctionBid.objects.aggregate(Sum('offer'))['offer__sum']
    # total_offers_k = total_offers // 1000
    you_win = Auction.objects.filter(winner=request.user).values('title', 'id')

    # get aggregate data
    top_5 = AuctionBid.objects.select_related('auction', 'bid').prefetch_related('user') \
                .values('auction__product__name', 'offer') \
                .annotate(Sum('offer')) \
                .order_by('-offer')[:5]

    top_5_offer_values = [item['offer'] for item in top_5]
    # top_5_offer_names = [item['auction__product__name'] for item in top_5]
    # top_5_offer_names = [name[:8] + '...' for name in top_5_offer_names]
    # you_win = [item['title'] for item in you_win]

    # store context
    context = {
        'total_products': total_products,
        'total_users': total_users,
        'total_auctions': total_auctions,
        'total_offers': total_offers,
        'top_5_offer_values': top_5_offer_values,
        'you_win': you_win,
        'url': reverse('system:auctions')
    }
    return render(request, 'dashboard.html', context)
