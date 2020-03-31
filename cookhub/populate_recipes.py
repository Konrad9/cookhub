# Initialise required Django infrastructure
import os


def populate():
    titles = ['Chicken soup', 'Pork belly stew', 'Monkey Brain toast', 'Chicken wing with beer', 'Life after death',
              'Pizza with pineapples', 'Duck breast with salmon eyeballs', 'Flamingo thighs']
    descriptions = ['Good to eat when you are feeling sick',
                    'This is a classic german dish, only recommended for those who have a strong stomach',
                    'One of the best Indonesian dishes ever created, would not recommend for anyone, pure animal cruelty',
                    'this is a great Slovenian staple food, usually consumes during the evening watching a game',
                    'No one knows what this dish is, just put everything you find at home in a pot and cook for 3 hours on low heat',
                    'Just no.', 'This is a bit weird as well, but hey, its got some nutrition in it. Eat it!',
                    'This dish has nothing in it, I mean have you seen a flamingo thighs before?!']
    times = [20, 460, 90, 15, 180, 0, 90, 60]
    servings = 4
    categories = ['Chicken', 'Pork', 'Monkey', 'Chicken', 'Death', 'Pizza', 'Duck', 'Flamingo']

    username = 'superuser'
    email = 'superuser@cookhub.com'
    password = 'TheMostSecurePassword'

    user = create_super_user(username, email, password)

    print('Superuser created')

    for i in range(8):
        category = createCategory(categories[i])
        recipe = createRecipe(titles[i], descriptions[i], times[i], servings, category, user)
        print(recipe)


def createCategory(category):
    cat = Category.objects.get_or_create(name=category)[0]
    # cat.save()
    return cat


def createRecipe(title, description, time, servings, category, user):
    recipe = Recipe.objects.get_or_create(title=title, description=description, time=time, servings=servings,
                                          user=user)[0]
    # recipe.categories.set('category')
    recipe.save()
    return recipe


def create_super_user(username, email, password):
    try:
        u = User.objects.create_superuser(username, email, password)
        return u
    except IntegrityError:
        return User.objects.filter(is_superuser=True)[0]


# This code will only run as a standalone script, not when imported
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cookhub_project.settings')

    import django

    django.setup()

    # import after Django has been initialised
    from cookhub.models import Recipe, Category
    from django.contrib.auth.models import User
    from django.db import IntegrityError

    print('Populating recipes...')
    populate()
    print('Done.')
