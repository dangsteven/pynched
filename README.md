# [pynched](http://pynched.com/)

[pynched](http://pynched.com/) is an open source project tracking and publishing amazon textbook prices over time. 

## The Code

pynched uses two main files for its data: getHTMLs.py and windowShopping.py (both in the getData folder). 
[getHTMLs](https://github.com/silkypanda/pynched/blob/gh-pages/getData/getHTML.py) retrieves all the data needed to scrape the site for price info. It is (ideally) only run once, at the beginning of the data collection.
[windowShopping](https://github.com/silkypanda/pynched/blob/gh-pages/getData/windowShopping.py) is run daily. It uses the identification material collected in getHTMLs to find the new, used, and trade-in prices and catalog them.

<!-- ## Bugs and Issues

Have a bug or an issue with this template? Let us know! [Open a new issue](https://github.com/IronSummitMedia/startbootstrap-sb-admin/issues) here on GitHub or leave a comment on the [template overview page at Start Bootstrap](http://startbootstrap.com/template-overviews/sb-admin/). -->

## Creators

pynched was created by and is maintained by **Steven Dang** and **Liz Furlan**.

* https://github.com/silkypanda
* https://github.com/eafurlan

We used and would like to thank: TheNewBoston's beautiful soup tutorial, beautiful soup itself, bootstrap, the amazon product api, the [amazon simple product api project](https://github.com/yoavaviram/python-amazon-simple-product-api), and [avi's post on stack overflow](http://codereview.stackexchange.com/questions/56554/python-script-which-fetches-amazon-product-details-using-its-api).
