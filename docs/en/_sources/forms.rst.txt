Forms
=====

Like django-localflavors the CPFField and CNPJField are validators to Brazilian CPF and CNPJ with a big difference, It removes repeated sequences and undue values.

Usage:

Your Just need to add your form class. Example using ModelForm:


CPFField
--------

.. code-block:: python

    from django_models.forms import CPFField

    ...

    class TestForm(forms.ModelForm):
        class Meta:
            model = YourModel

        fields = [..., 'cpf']
        widgets = {
            'cpf': CNPJField(),
        }




CNPJField
---------

.. code-block:: python

    from django_models.forms import CNPJField

    ...

    class TestForm(forms.ModelForm):
        class Meta:
            model = YourModel

        fields = [..., 'cnpj']
        widgets = {
            'cnpj': CNPJField(),
        }

