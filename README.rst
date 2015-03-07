============
Starbucks-py
============

.. image:: https://pypip.in/v/Starbucks/badge.svg
    :target: https://pypi.python.org/pypi/Starbucks/

Unofficial Starbucks API.

This API is written in Python.

*Only supports for Starbucks Korea.*


Installation
------------

You can install Starbucks with ``pip``

::

    $ pip install starbucks



Features
--------

1. Login
~~~~~~~~

You can login to Starbucks like:

::

    from starbucks import Starbucks
    
    starbucks = Starbucks()
    starbucks.login('username', 'password')
    


2. Get My Cards
~~~~~~~~~~~~~~~

You can get your cards like:

::

    cards = starbucks.get_cards()



3. Get My Card Information
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can get your card information like:

::

    # You should know the registration number of your card.
    # It is in the source code of Starbucks web page.
    card = starbucks.get_card_info('0000000')
    
or using CLI:

::

    $ starbucks-card --id {username} --password {password} --reg-number {card reg number}



4. Get My Stars Count
~~~~~~~~~~~~~~~~~~~~~

You can get your stars count like:

::

    starbucks.get_stars_count()
    
or using CLI:

::

    $ starbucks-star --id {username} --password {password}
    


5. Get Beverage Menus
~~~~~~~~~~~~~~~~~~~~~

You can get the list of beverage menus like:

::

    starbucks.get_beverages()



6. Get My Coupons
~~~~~~~~~~~~~~~~~~~~~

You can get the list of your coupons like:

::

    starbucks.get_coupons()
    


7. Logout
~~~~~~~~~

If you want to logout, just:

::

    starbucks.logout()
    


Known Issues
------------

- Should I have to check if I logged in successfully like this?


To Do
-----

- Card usage histories
- More error checks
- and so on.
