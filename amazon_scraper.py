# Various functions to retrieve specific data we want from Amazon

# Function to extract Product Title
def get_title(soup: str) -> str:
    try:
        title = soup.find("span", attrs={"id":'productTitle'}).text.strip()

    except AttributeError:
        title = ""

    return title

# Function to extract Product Price
def get_price(soup: str) -> str:
    try:
        price = soup.find("span", attrs={'id':'price'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'class':'a-price a-text-price header-price a-size-base a-text-normal'})
            price = price.find("span", attrs={'class':'a-offscreen'}).string.strip()
        except AttributeError:
            try:
                price = soup.find("span", attrs={'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
                price = price.find("span", attrs={'class':'a-offscreen'}).string.strip()
            except AttributeError:
                price = ""
    return price

# Function to extract Product Rating
def get_rating(soup: str) -> str:
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup: str) -> str:
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup: str) -> str:
    try:
        availability = soup.find("div", attrs={'id':'availability'})
        availability = availability.find("span").string.strip()

    except AttributeError:
        availability = ""

    return availability
