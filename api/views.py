import time

from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import *
from .serializers import *

from archive.recognition import recognition


class RecognitionView(CreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = photos.objects.all()
    serializer_class = RecognitionSerializer

    def post(self, request, *args, **kwargs):
        serializer = RecognitionSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save(name=request.user)   # сначала сохраняет name как Anonymous
            photo_path = str(user_profile.photo)   # Преобразует путь в str
            car_fname_file = photo_path.split('/')[-1]
            print(car_fname_file)
            ans = recognition(car_fname_file)    # Использует нужную функцию
            user_profile.model_recognition = ans    # Сохраняет полученное значение из функции
            user_profile.save()    # Сохраняет данные в БД

            return Response(serializer.data['model_recognition'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyView(CreateAPIView):
    queryset = company.objects.all()
    serializer_class = CompanySerializer

    def get(self, request):
        comp = company.objects.all()

        page = self.paginate_queryset(comp)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializers = CompanySerializer(comp, many=True)
        return Response({'Company': serializers.data})

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:  # Проверить, является ли пользователь администратором
            return super().post(request, *args, **kwargs)  # Разрешить доступ
        else:
            return Response({"detail": "Учетные данные не были предоставлены."}, status=403)


class CompanyViewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]


class ModelView(CreateAPIView):
    queryset = car_model.objects.all()
    serializer_class = ModelSerializer

    def get(self, request, name):
        comp = get_object_or_404(company, id=name)
        model = comp.car_model_set.all()

        page = self.paginate_queryset(model)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializers = ModelSerializer(model, many=True)
        return Response({f'{comp.title}': serializers.data})

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:  # Проверить, является ли пользователь администратором
            return super().post(request, *args, **kwargs)  # Разрешить доступ
        else:
            return Response({"detail": "Учетные данные не были предоставлены."}, status=403)

    def perform_create(self, serializer):
        name = self.kwargs.get('name')

        # нужно переопределить чтобы в post запросе не указывать company_id, то есть марку авто
        comp = get_object_or_404(company, id=name)
        serializer.save(company_id=comp)


class ModelViewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = car_model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        name = self.kwargs.get('name')
        pk = self.kwargs.get('pk')

        comp = get_object_or_404(company, id=name)
        model = get_object_or_404(comp.car_model_set, id=pk)
        return model


class GenerationView(CreateAPIView):
    queryset = generations.objects.all()
    serializer_class = GenerationSerializer

    def get(self, request, name, gen):
        comp = get_object_or_404(company, id=name)
        model = get_object_or_404(comp.car_model_set, id=gen)
        ge = model.generations_set.all()

        page = self.paginate_queryset(ge)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(ge, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:  # Проверить, является ли пользователь администратором
            return super().post(request, *args, **kwargs)  # Разрешить доступ
        else:
            return Response({"detail": "Учетные данные не были предоставлены."}, status=403)

    def perform_create(self, serializer):
        name = self.kwargs.get('name')
        gen = self.kwargs.get('gen')

        comp = get_object_or_404(company, id=name)
        model = get_object_or_404(comp.car_model_set, id=gen)
        serializer.save(car_model_id=model)


class GenerationViewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = generations.objects.all()
    serializer_class = GenerationSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        name = self.kwargs.get('name')
        gen = self.kwargs.get('gen')
        pk = self.kwargs.get('pk')

        comp = get_object_or_404(company, id=name)
        model = get_object_or_404(comp.car_model_set, id=gen)
        ge = get_object_or_404(model.generations_set, id=pk)

        return ge


class EngineView(GenericAPIView):
    queryset = engines.objects.all()
    serializer_class = EngineSerializer

    def get(self, request, name, gen, eng):
        comp = get_object_or_404(company, id=name)
        model = get_object_or_404(comp.car_model_set, id=gen)
        ge = get_object_or_404(model.generations_set, id=eng)
        engines = ge.engine.all()

        page = self.paginate_queryset(engines)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializers = EngineSerializer(engines, many=True)
        return Response({f'{ge.title} {ge.year_start} - {ge.year_end}': serializers.data})


class EngineViewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = engines.objects.all()
    serializer_class = EngineSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        name = self.kwargs.get('name')
        gen = self.kwargs.get('gen')
        eng = self.kwargs.get('eng')
        pk = self.kwargs.get('pk')

        comp = get_object_or_404(company, id=name)
        model = get_object_or_404(comp.car_model_set, id=gen)
        ge = get_object_or_404(model.generations_set, id=eng)
        engines = get_object_or_404(ge.engine, id=pk)

        return engines


class EngineParamsView(GenericAPIView):
    # queryset = engine_params.objects.all()
    # serializer_class = EngineParamSerializer

    def get(self, request, name, gen, eng, eng_par):
        comp = get_object_or_404(company, id=name)
        model = get_object_or_404(comp.car_model_set, id=gen)
        ge = get_object_or_404(model.generations_set, id=eng)
        eng = get_object_or_404(ge.engine, id=eng_par)
        params = get_object_or_404(engine_params, id=eng.id)

        serializers = EngineParamSerializer(params)
        return Response({f'{params.name}': serializers.data})


class AllModelView(ReadOnlyModelViewSet):
    queryset = car_model.objects.all()
    serializer_class = ModelSerializer


class AllGenView(ReadOnlyModelViewSet):
    queryset = generations.objects.all()
    serializer_class = GenerationSerializer


class AllEngineView(ModelViewSet):
    queryset = engines.objects.all()
    serializer_class = EngineSerializer


class AllParamsView(ModelViewSet):
    queryset = engine_params.objects.all()
    serializer_class = EngineParamSerializer
