class setSerializerByMethodMixin:
    serializer_by_method = None

    def get_serializer_class(self):

        assert (
            self.serializer_by_method is not None
        ), f"'{self.__class__.__name__}' should include a `serializer_by_method` attribute."

        return self.serializer_by_method.get(self.request.method, self.serializer_class)
