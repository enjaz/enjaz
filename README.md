student-portal
==============

The Student Portal is a [Django-based](https://www.djangoproject.com)
platform for university student activity.  Through the platform,
students can submit activities for approval, join clubs, enter their
'Activity Points' (Niqati) and contribute and borrow books.

# Licensing

* Copyright (C) 2014-2017 [Osama Khalid](https://osamakhalid.com)
* Copyright (C) 2014-2015 Muhammad Saeed Arabi
* Copyright (C) 2016-2017 Abdulrahman Abdullah Alsalim
* Copyright (C) 2016-2017 [Amjaad Abdullah](https://amjaadabdullah.com/blog/)
* Copyright (C) 2016-2017 Zaha al-Jamaan

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Affero General Public License for more details.
```

Additionally, the `studentvoice` app includes parts from the Askbot
project.

* Copyright (C) 2009 Chen Gang and Sailing Cai.
* Copyright (C) 2009-2011 Evgeny Fadeev and individual contributors of Askbot project

The `forms_builder` app is a modified version of django-forms-builder by Stephen McDonald.

* Copyright (C) Stephen McDonald and individual contributors.

Licensed under the General Public License version 3 of the License, or
(at your option) any later version.

# Installation 

Enjaz Portal works with Python 2.7 and Django 1.8.

## Get it!

Get the code using git:

```
git clone https://github.com/osamak/student-portal.git enjaz
cd enjaz
```

Then install all the dependencies using:

```pip install --user -r requirements.txt```

## Set it up!

Copy `enjaz/enjaz/secrets.template.py`  to `enjaz/enjaz/secrets.py`.

The only required setting in `secrets.py` is `SECRET_KEY` which can be generated using [this tool](http://www.miniwebtool.com/django-secret-key-generator/).

Then get the database sorted out, by migrating:

```python manage.py migrate```

Then import sites, categories and email templates:

```python manage.py loaddata core/fixtures/default_emailtemplates.json core/fixtures/default_sites.json activities/fixtures/default_categories.json```

Finally, create userena permissions using:

```python manage.py check_permissions```

## Then enjoy!