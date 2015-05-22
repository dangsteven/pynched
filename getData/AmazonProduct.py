class AmazonProduct(LXMLWrapper):
    """A wrapper class for an Amazon product.
    """

    def __init__(self, item, aws_associate_tag, api, *args, **kwargs):
        """Initialize an Amazon Product Proxy.
        :param item:
            Lxml Item element.
        """
        super(AmazonProduct, self).__init__(item)
        self.aws_associate_tag = aws_associate_tag
        self.api = api
        self.parent = None
        self.region = kwargs.get('region', 'US')

    @property
    def price_and_currency(self):
        """Get Offer Price and Currency.
        Return price according to the following process:
        * If product has a sale return Sales Price, otherwise,
        * Return Price, otherwise,
        * Return lowest offer price, otherwise,
        * Return None.
        :return:
            A tuple containing:
                1. Float representation of price.
                2. ISO Currency code (string).
        """
        price = self._safe_get_element_text(
            'Offers.Offer.OfferListing.SalePrice.Amount')
        if price:
            currency = self._safe_get_element_text(
                'Offers.Offer.OfferListing.SalePrice.CurrencyCode')
        else:
            price = self._safe_get_element_text(
                'Offers.Offer.OfferListing.Price.Amount')
            if price:
                currency = self._safe_get_element_text(
                    'Offers.Offer.OfferListing.Price.CurrencyCode')
            else:
                price = self._safe_get_element_text(
                    'OfferSummary.LowestNewPrice.Amount')
                currency = self._safe_get_element_text(
                    'OfferSummary.LowestNewPrice.CurrencyCode')
        if price:
            fprice = float(price) / 100 if 'JP' not in self.region else price
            return fprice, currency
        else:
            return None, None

    @property
    def asin(self):
        """ASIN (Amazon ID)
        :return:
            ASIN (string).
        """
        return self._safe_get_element_text('ASIN')

    @property
    def sales_rank(self):
        """Sales Rank
        :return:
            Sales Rank (integer).
        """
        return self._safe_get_element_text('SalesRank')

    @property
    def offer_url(self):
        """Offer URL
        :return:
            Offer URL (string).
        """
        return "{0}{1}/?tag={2}".format(
            AMAZON_ASSOCIATES_BASE_URL.format(domain=DOMAINS[self.region]),
            self.asin,
            self.aws_associate_tag)

    @property
    def author(self):
        """Author.
        Depricated, please use `authors`.
        :return:
            Author (string).
        """
        authors = self.authors
        if len(authors):
            return authors[0]
        else:
            return None

    @property
    def authors(self):
        """Authors.
        :return:
            Returns of list of authors
        """
        result = []
        authors = self._safe_get_element('ItemAttributes.Author')
        if authors is not None:
            for author in authors:
                result.append(author.text)
        return result

    @property
    def creators(self):
        """Creators.
        Creators are not the authors. These are usually editors, translators,
        narrators, etc.
        :return:
            Returns a list of creators where each is a tuple containing:
                1. The creators name (string).
                2. The creators role (string).
        """
        # return tuples of name and role
        result = []
        creators = self._safe_get_element('ItemAttributes.Creator')
        if creators is not None:
            for creator in creators:
                role = creator.attrib['Role'] if 'Role' in creator.attrib else None
                result.append((creator.text, role))
        return result

    @property
    def publisher(self):
        """Publisher.
        :return:
            Publisher (string)
        """
        return self._safe_get_element_text('ItemAttributes.Publisher')

    @property
    def label(self):
        """Label.
        :return:
            Label (string)
        """
        return self._safe_get_element_text('ItemAttributes.Label')

    @property
    def manufacturer(self):
        """Manufacturer.
        :return:
            Manufacturer (string)
        """
        return self._safe_get_element_text('ItemAttributes.Manufacturer')

    @property
    def brand(self):
        """Brand.
        :return:
            Brand (string)
        """
        return self._safe_get_element_text('ItemAttributes.Brand')

    @property
    def isbn(self):
        """ISBN.
        :return:
            ISBN (string)
        """
        return self._safe_get_element_text('ItemAttributes.ISBN')

    @property
    def eisbn(self):
        """EISBN (The ISBN of eBooks).
        :return:
            EISBN (string)
        """
        return self._safe_get_element_text('ItemAttributes.EISBN')

    @property
    def binding(self):
        """Binding.
        :return:
            Binding (string)
        """
        return self._safe_get_element_text('ItemAttributes.Binding')

    @property
    def pages(self):
        """Pages.
        :return:
            Pages (string)
        """
        return self._safe_get_element_text('ItemAttributes.NumberOfPages')

    @property
    def publication_date(self):
        """Pubdate.
        :return:
            Pubdate (datetime.date)
        """
        return self._safe_get_element_date('ItemAttributes.PublicationDate')

    @property
    def release_date(self):
        """Release date .
        :return:
            Release date (datetime.date)
        """
        return self._safe_get_element_date('ItemAttributes.ReleaseDate')

    @property
    def edition(self):
        """Edition.
        :return:
            Edition (string)
        """
        return self._safe_get_element_text('ItemAttributes.Edition')

    @property
    def large_image_url(self):
        """Large Image URL.
        :return:
            Large image url (string)
        """
        return self._safe_get_element_text('LargeImage.URL')

    @property
    def medium_image_url(self):
        """Medium Image URL.
        :return:
            Medium image url (string)
        """
        return self._safe_get_element_text('MediumImage.URL')

    @property
    def small_image_url(self):
        """Small Image URL.
        :return:
            Small image url (string)
        """
        return self._safe_get_element_text('SmallImage.URL')

    @property
    def tiny_image_url(self):
        """Tiny Image URL.
        :return:
            Tiny image url (string)
        """
        return self._safe_get_element_text('TinyImage.URL')

    @property
    def reviews(self):
        """Customer Reviews.
        Get a iframe URL for customer reviews.
        :return:
            A tuple of: has_reviews (bool), reviews url (string)
        """
        iframe = self._safe_get_element_text('CustomerReviews.IFrameURL')
        has_reviews = self._safe_get_element_text('CustomerReviews.HasReviews')
        if has_reviews and has_reviews == 'true':
            has_reviews = True
        else:
            has_reviews = False
        return has_reviews, iframe

    @property
    def ean(self):
        """EAN.
        :return:
            EAN (string)
        """
        ean = self._safe_get_element_text('ItemAttributes.EAN')
        if ean is None:
            ean_list = self._safe_get_element_text('ItemAttributes.EANList')
            if ean_list:
                ean = self._safe_get_element_text(
                    'EANListElement', root=ean_list[0])
        return ean

    @property
    def upc(self):
        """UPC.
        :return:
            UPC (string)
        """
        upc = self._safe_get_element_text('ItemAttributes.UPC')
        if upc is None:
            upc_list = self._safe_get_element_text('ItemAttributes.UPCList')
            if upc_list:
                upc = self._safe_get_element_text(
                    'UPCListElement', root=upc_list[0])
        return upc

    @property
    def color(self):
        """Color.
        :return:
            Color (string)
        """
        return self._safe_get_element_text('ItemAttributes.Color')

    @property
    def sku(self):
        """SKU.
        :return:
            SKU (string)
        """
        return self._safe_get_element_text('ItemAttributes.SKU')

    @property
    def mpn(self):
        """MPN.
        :return:
            MPN (string)
        """
        return self._safe_get_element_text('ItemAttributes.MPN')

    @property
    def model(self):
        """Model Name.
        :return:
            Model (string)
        """
        return self._safe_get_element_text('ItemAttributes.Model')

    @property
    def part_number(self):
        """Part Number.
        :return:
            Part Number (string)
        """
        return self._safe_get_element_text('ItemAttributes.PartNumber')

    @property
    def title(self):
        """Title.
        :return:
            Title (string)
        """
        return self._safe_get_element_text('ItemAttributes.Title')

    @property
    def editorial_review(self):
        """Editorial Review.
        Returns an editorial review text.
        :return:
            Editorial Review (string)
        """
        reviews = self.editorial_reviews
        if reviews:
            return reviews[0]
        return ''

    @property
    def editorial_reviews(self):
        """Editorial Review.
        Returns a list of all editorial reviews.
        :return:
            A list containing:
                Editorial Review (string)
        """
        result = []
        reviews_node = self._safe_get_element('EditorialReviews')

        if reviews_node is not None:
            for review_node in reviews_node.iterchildren():
                content_node = getattr(review_node, 'Content')
                if content_node is not None:
                    result.append(content_node.text)
        return result

    @property
    def languages(self):
        """Languages.
        Returns a set of languages in lower-case.
        :return:
            Returns a set of languages in lower-case (strings).
        """
        result = set()
        languages = self._safe_get_element('ItemAttributes.Languages')
        if languages is not None:
            for language in languages.iterchildren():
                text = self._safe_get_element_text('Name', language)
                if text:
                    result.add(text.lower())
        return result

    @property
    def features(self):
        """Features.
        Returns a list of feature descriptions.
        :return:
            Returns a list of 'ItemAttributes.Feature' elements (strings).
        """
        result = []
        features = self._safe_get_element('ItemAttributes.Feature')
        if features is not None:
            for feature in features:
                result.append(feature.text)
        return result

    @property
    def list_price(self):
        """List Price.
        :return:
            A tuple containing:
                1. Float representation of price.
                2. ISO Currency code (string).
        """
        price = self._safe_get_element_text('ItemAttributes.ListPrice.Amount')
        currency = self._safe_get_element_text(
            'ItemAttributes.ListPrice.CurrencyCode')
        if price:
            return float(price) / 100, currency
        else:
            return None, None

    def get_attribute(self, name):
        """Get Attribute
        Get an attribute (child elements of 'ItemAttributes') value.
        :param name:
            Attribute name (string)
        :return:
            Attribute value (string) or None if not found.
        """
        return self._safe_get_element_text("ItemAttributes.{0}".format(name))

    def get_attribute_details(self, name):
        """Get Attribute Details
        Gets XML attributes of the product attribute. These usually contain
        details about the product attributes such as units.
        :param name:
            Attribute name (string)
        :return:
            A name/value dictionary.
        """
        return self._safe_get_element("ItemAttributes.{0}".format(name)).attrib

    def get_attributes(self, name_list):
        """Get Attributes
        Get a list of attributes as a name/value dictionary.
        :param name_list:
            A list of attribute names (strings).
        :return:
            A name/value dictionary (both names and values are strings).
        """
        properties = {}
        for name in name_list:
            value = self.get_attribute(name)
            if value is not None:
                properties[name] = value
        return properties

    @property
    def parent_asin(self):
        """Parent ASIN.
        Can be used to test if product has a parent.
        :return:
            Parent ASIN if product has a parent.
        """
        return self._safe_get_element('ParentASIN')

    def get_parent(self):
        """Get Parent.
        Fetch parent product if it exists.
        Use `parent_asin` to check if a parent exist before fetching.
        :return:
            An instance of :class:`~.AmazonProduct` representing the
            parent product.
        """
        if not self.parent:
            parent = self._safe_get_element('ParentASIN')
            if parent:
                self.parent = self.api.lookup(ItemId=parent)
        return self.parent

    @property
    def browse_nodes(self):
        """Browse Nodes.
        :return:
            A list of :class:`~.AmazonBrowseNode` objects.
        """
        root = self._safe_get_element('BrowseNodes')
        if root is None:
            return []

        return [AmazonBrowseNode(child) for child in root.iterchildren()]

    @property
    def images(self):
        """List of images for a response.
        When using lookup with RespnoseGroup 'Images', you'll get a list of images.
        Parse them so they are returned in an easily used list format.
        :return:
            A list of `ObjectifiedElement` images
        """
        try:
            images = [image for image in self._safe_get_element('ImageSets.ImageSet')]
        except TypeError:  # No images in this ResponseGroup
            images = []
        return images