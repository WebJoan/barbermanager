from ninja import Router

router = Router()

@router.get("/")
def barber_placeholder(request):
    """
    Placeholder for barber endpoints - will be implemented soon
    """
    return {"message": "Barber endpoints under construction"} 