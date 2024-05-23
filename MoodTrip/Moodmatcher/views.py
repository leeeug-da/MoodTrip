# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm, CommentForm, PostUpdateForm, ImageUploadForm
from .models import Post, Comment, Profile, PostLike, TouristSpot
from django.http import HttpResponse, JsonResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from django.conf import settings
import os
import random
import time
import pandas as pd
import traceback
from django.views.generic import TemplateView
from .models import SelectedImage
import logging
from .models import UploadedImage
from .models import TourCategory

from tensorflow.keras.optimizers import Adam
from pathlib import Path
import shutil
from Moodmatcher.models import TourKeyRat, TourMain, TourInfo, TourPeriod, TourEtc, TourImgPath
from urllib.parse import quote
from django.http import JsonResponse
from django.http import HttpResponse
import urllib.parse
from django.core.files.storage import FileSystemStorage

# 모델
model_path = os.path.join(settings.BASE_DIR, "Moodmatcher/models/TL_inception.h5")
loaded_model = load_model(model_path, compile=False)
# loaded_model = load_model(model_path)


def main_page(request):
    return render(request, 'Moodmatcher/main.html')

def service_intro(request):
    return render(request, 'Moodmatcher/service_intro.html')

def recommend_view(request):
    return render(request, 'Moodmatcher/recommend_overview.html')

def image_choice_recommend(request):
    if request.method == 'POST':
        selected_images = request.POST.getlist('selected_images')
        # 여기서 select 된 이미지를 특정 디렉터리에 복사하도록 (media directory )
        if len(selected_images) > 3:
            return HttpResponse("이미지를 정확히 3개 선택해주세요.")
        print(selected_images)
        sel_imgF = []
        for im in selected_images :
            fileN = im.split('/')[-1]
            print(fileN)
            sel_imgF.append(fileN)
            shutil.copyfile(im,'/home/lab09/MoodTrip/media/randomImg/'+fileN)
        recommended_spots = recommend_tourist_spots(selected_images)

        # 세션에서 이미지 세트를 가져옴
        random_images_paths = request.session.get('random_images_paths', get_random_images_per_folder(2))

        return render(request, 'Moodmatcher/image_choice_recommend_result.html',
                      {'selected_images': sel_imgF, 'recommended_spots': recommended_spots,
                       'random_images': random_images_paths})

    # 세션에서 이미지 세트를 가져옴
    random_images_paths = request.session.get('random_images_paths', get_random_images_per_folder(2))

    return render(request, 'Moodmatcher/image_choice_recommend.html', {'random_images': random_images_paths})





# 랜덤하게 중복 없이 이미지 선택하는 함수
def get_unique_random_images(image_list, count):
    if len(image_list) <= count:
        return image_list
    else:
        return random.sample(image_list, count)


def recommend_tourist_spots(selected_images):
    try:
        # 모델 로드
        model_path = os.path.join(settings.BASE_DIR, "Moodmatcher/models/TL_inception.h5")
        loaded_model = load_model(model_path,compile=False)

        # 이미지 분석 및 예측 결과 저장
        predictions_per_image = []
        for img_path in selected_images:
            prediction = analyze_image(loaded_model, img_path)            
            predictions_per_image.append(prediction)

        print(predictions_per_image)

        # 예측 결과 평균 계산
        average_predictions = np.mean(predictions_per_image, axis=0)

        # 특정 조건에 따라 가중치를 부여하여 최종 점수 계산 및 가장 높은 점수의 카테고리 선택
        selected_categories = get_top_categories(average_predictions)

        # 테이블에서 데이터 읽어오기
        tour_key_rats_all = TourKeyRat.objects.all()

        # 추천 관광지 리스트를 반환 (각 카테고리별로 상위 10개씩 반환)
        recommended_spots = []
        for index, category in enumerate(selected_categories):
            tour_key_rats_filtered = tour_key_rats_all.filter(key_1=category).order_by('-ratings')[:9]
            recommended_spots.extend([
                {
                    'index': tour_key_rat.tour_id,
                    'tour': tour_key_rat.tour_id,
                    'tour_cat': tour_key_rat.tour_cat_id,
                    'key_1': tour_key_rat.key_1,
                    'ratings': tour_key_rat.ratings,
                    'Tourist_Spot_Name': tour_key_rat.tour.name
                } 
                for tour_key_rat in tour_key_rats_filtered
            ])
        print(recommended_spots)
        return recommended_spots
    except Exception as e:
        print(f"An exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return []



def analyze_image(model, img_path):
    try:
        # 이미지 전처리
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # 디버깅 메시지 추가
        print(f"Image path: {img_path}")
        print(f"Image array shape: {img_array.shape}")

        # 이미지 예측
        predictions = model.predict(img_array)
        return predictions.flatten()  # 1차원 배열로 변환하여 반환
    except Exception as e:
        print(f"Error occurred during image analysis: {e}")
        return None  # 예측에 실패하면 None 반환



def get_top_categories(predictions):
    categories = ["joyful", "adventure", "tradition", "nature", "cultural", "art"]
    keyword_weights = {"joyful": 0.3, "adventure": 0.2, "tradition": 0.1, "nature": 0.1, "cultural": 0.3, "art": 0.2}

    # 예측된 확률 중 상위 3개 키워드 선택
    top_categories = np.array(categories)[np.argsort(predictions)[::-1][:3]]

    # 상위 1번과 상위 2번의 예측 확률 차이가 10% 미만이면 가중치 부여
    if predictions[categories.index(top_categories[0])] - predictions[categories.index(top_categories[1])] < 0.1:
        for i in range(len(top_categories)):
            # 가중치 부여
            predictions[categories.index(top_categories[i])] *= keyword_weights.get(top_categories[i], 1.0)

    return top_categories



def get_random_image_urls():
    # 각 폴더에서 선택할 이미지 수 정의
    images_per_folder = 2

    # 선택된 이미지 URL을 저장할 리스트 생성
    random_image_urls = []

    # 각 폴더를 반복
    for i in range(0, 7):  # "folder1", "folder2", ..., "folder6"가 있는 경우
        folder_name = f'folder{i}'
        # image_dir = os.path.join(settings.BASE_DIR, f'ambience_img/{folder_name}/')
        image_dir = os.path.join(Path(settings.BASE_DIR).parent, 'ambience_img', folder_name)  # Updated path
        image_files = [f"{settings.BASE_URL}{folder_name}/{image}" for image in os.listdir(image_dir) if image.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # 폴더에서 랜덤 이미지 선택
        random_images = get_unique_random_images(image_files, images_per_folder)

        # 선택된 이미지를 리스트에 추가
        random_image_urls.extend(random_images)

    return random_image_urls


import random

def get_random_images_per_folder(images_per_folder):
    categories = ["adventure", "art", "joyful", "cultural", "nature", "tradition"]
    random_image_urls = []

    for category in categories:
        # image_dir = os.path.join(settings.BASE_DIR, f'ambience_img/{category}/')
        image_dir = os.path.join(Path(settings.BASE_DIR).parent, 'ambience_img', category)  # Updated path
        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # 각 폴더에서 랜덤 이미지 2개씩 선택
        random_images = get_unique_random_images(image_files, images_per_folder)
        random_images_paths = [os.path.join(image_dir, img) for img in random_images]

        random_image_urls.extend(random_images_paths)

    return random_image_urls


def random_image(request):
    # 세션에서 이미지 세트를 가져옴
    random_images_paths = request.session.get('random_images_paths', get_random_images_per_folder(2))

    # 랜덤 이미지 중에서 요청받은 이미지를 선택
    random_image_path = random.choice(random_images_paths)

    # 선택된 이미지를 HttpResponse로 반환
    with open(random_image_path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type='image/jpeg')
        response['Content-Disposition'] = 'inline; filename=' + random_image_path.split('/')[-1]

    return response


@login_required(login_url='/login/')
def image_upload_recommend(request): 
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_obj = UploadedImage(image=form.cleaned_data['image'])
            # image_obj.user = request.user
            # image_obj.save()

            img_path = image_obj.image.path
            # img_path='/home/lab09/MoodTrip/media/images/20231015_152352.jpg'
            print("Image path:", img_path)  # 디버깅 메시지 추가
            prediction = analyze_image(loaded_model, img_path)
            
            if prediction is not None:
                recommended_spots = [{'tourist_spot_name': '추천 관광지', 'top_keywords': prediction}]
                print(recommended_spots)
                # return HttpResponse(recommended_spots)
                return render(request, 'Moodmatcher/image_upload_recommend_result.html', {'recommended_spots': recommended_spots})
            else:
                messages.error(request, "이미지 분석에 실패했습니다.")
        else:
            print("Form is not valid:", form.errors)  # 디버깅 메시지 추가
            messages.error(request, "이미지 업로드에 실패하였습니다. 다시 시도해주세요.")
    else:
        form = ImageUploadForm()

    return render(request, 'Moodmatcher/image_upload_recommend.html', {'form': form})




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'Moodmatcher/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.error(request, "아이디나 비밀번호가 일치하지 않습니다.")
    else:
        form = AuthenticationForm()
    return render(request, 'Moodmatcher/login.html', {'form': form})


@login_required(login_url='/login/')
def community(request):
    posts = Post.objects.filter(category='community').order_by('-created_at')
    return render(request, 'Moodmatcher/community.html', {'posts': posts})


def customer_service(request):
    posts = Post.objects.filter(category='customer-service').order_by('-created_at')
    return render(request, 'Moodmatcher/customer_service.html', {'posts': posts})


def post_detail(request, category, post_id):
    post = get_object_or_404(Post, id=post_id, category=category)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()

    post.views += 1
    post.save()

    return render(request, 'Moodmatcher/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'category': category})


@login_required(login_url='/login/')
def post_create(request, category):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = category
            post.save()
            return redirect('community' if category == 'community' else 'customer_service')
    else:
        form = PostForm()
    return render(request, 'Moodmatcher/post_create.html', {'form': form, 'category': category})


@login_required(login_url='/login/')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, '댓글이 성공적으로 작성되었습니다.')
    return redirect('post_detail', category=post.category, post_id=post.id)


@login_required(login_url='/login/')
def post_update(request, category, post_id):
    post = get_object_or_404(Post, id=post_id, category=category, author=request.user)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '게시글이 성공적으로 수정되었습니다.')
            return redirect('post_detail', category=category, post_id=post_id)
    else:
        form = PostUpdateForm(instance=post)
    return render(request, 'Moodmatcher/post_update.html', {'form': form, 'category': category, 'post_id': post_id})


@login_required(login_url='/login/')
def post_delete(request, category, post_id):
    post = get_object_or_404(Post, id=post_id, category=category, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '게시글이 성공적으로 삭제되었습니다.')
        return redirect('community' if category == 'community' else 'customer_service')
    return render(request, 'Moodmatcher/post_delete.html', {'post': post, 'category': category})


@login_required(login_url='/login/')
def post_create_customer_service(request, category):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = category
            post.save()
            return redirect('customer_service')
    else:
        form = PostForm()
    return render(request, 'Moodmatcher/post_create_customer_service.html', {'form': form, 'category': category})


@login_required(login_url='/login/')
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', category=comment.post.category, post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'Moodmatcher/comment_update.html', {'form': form, 'comment': comment})


@login_required(login_url='/login/')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        comment.delete()
        messages.success(request, '댓글이 성공적으로 삭제되었습니다.')
        return redirect('post_detail', category=comment.post.category, post_id=comment.post.id)
    return render(request, 'Moodmatcher/comment_delete.html', {'comment': comment})


@login_required
def my_profile(request):
    user = request.user
    comments = Comment.objects.filter(author=user)
    posts = Post.objects.filter(author=user)
    liked_posts = request.user.liked_posts.all()
    all_posts = Post.objects.all()
    liked_post_objects = Post.objects.filter(id__in=liked_posts)

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    context = {
        'user': user,
        'profile': profile,
        'comments': comments,
        'posts': posts,
        'liked_posts': liked_post_objects,
    }

    return render(request, 'Moodmatcher/my_profile.html', context)


@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    post.new_likes = post.likes.count()
    post.save()

    liked_posts = Post.objects.filter(id__in=request.user.postlike_set.values_list('post_id', flat=True))
    all_posts = Post.objects.all()

    return render(request, 'Moodmatcher/post_detail.html', {'post': post, 'category': post.category, 'liked_posts': liked_posts, 'all_posts': all_posts})




def image_choice_recommend_result(request):
    selected_images = SelectedImage.objects.all()
    recommended_spots = recommend_tourist_spots([image.path for image in selected_images])
    return render(request, 'Moodmatcher/image_choice_recommend_result.html',
                  {'selected_images': selected_images, 'recommended_spots': recommended_spots})

def image_upload_recommend_result(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('uploaded_image')

        try:
            prediction = analyze_image(loaded_model, uploaded_image)
            recommended_spot = {'tourist_spot_name': '추천 관광지', 'top_keywords': prediction}

            # 이미지 업로드 추천 결과를 JSON으로 반환
            return render(request, 'Moodmatcher/image_upload_recommend_result.html', {'uploaded_image': uploaded_image, 'recommended_spot': recommended_spot})
        except Exception as e:
            messages.error(request, f"이미지 분석에 실패했습니다: {e}")
            return redirect('image_upload_recommend')

    return redirect('image_upload_recommend')



def upload_image(request):
    try:
        if request.method == 'POST' and request.FILES['image']:
            # 업로드된 이미지 가져오기
            uploaded_image = request.FILES['image']

            # 여기에 처리 또는 저장 로직을 수행

            # 성공 응답 반환
            return JsonResponse({'success': True, 'message': '이미지가 성공적으로 업로드되었습니다!'})
        else:
            # 이미지가 제공되지 않았을 때 오류 응답 반환
            return JsonResponse({'success': False, 'error_message': '업로드할 이미지가 제공되지 않았습니다.'})
    except Exception as e:
        # 다른 예외에 대한 오류 응답 반환
        return JsonResponse({'success': False, 'error_message': str(e)})
    

###############
class ImageRecommendResultView(TemplateView):
    template_name = 'image_choice_recommend_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # SelectedImage 모델에서 최근 업로드된 이미지들을 가져오기
        selected_images = SelectedImage.objects.all().order_by('-uploaded_at')[:3]

        # 추천된 관광지 계산
        recommended_spots = recommend_tourist_spots([image.path for image in selected_images])

        context['selected_images'] = selected_images
        context['recommended_spots'] = recommended_spots

        return context


########관광지 정보



def recommend_tourist_spots_from_images(request):
    try:
        # 엑셀 파일에서 데이터 읽어오기
        df = pd.read_excel('C:/Users/김현/Desktop/MoodTrip/tourist_keywords.xlsx')

        # 평점에 따라 내림차순으로 정렬
        df_sorted = df.sort_values(by='평점', ascending=False)

        # 각 키워드별로 상위 몇 개의 관광지를 선택하여 추천 목록 생성
        keyword_recommendations = {}
        num_recommendations = 3  # 각 키워드당 추천할 관광지 수

        for keyword in df_sorted['Top_Keyword'].unique():
            keyword_df = df_sorted[df_sorted['Top_Keyword'] == keyword].head(num_recommendations)
            recommendations = keyword_df['Tourist_Spot_Name'].tolist()
            keyword_recommendations[keyword] = recommendations

        # 추천 목록을 템플릿에 전달하여 렌더링
        return render(request, 'recommendations.html', {'keyword_recommendations': keyword_recommendations})

    except Exception as e:
        print(f"An exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return render(request, 'error.html', {'error_message': '오류가 발생했습니다.'})
    



def load_travel_data():
    data = pd.read_excel('C:/Users/김현/Desktop/MoodTrip/travel_data_idx.xlsx')
    return data.to_dict('records')  # list of dictionaries 형태로 변환


def my_view(request):
    travel_data = load_travel_data()
    return render(request, 'my_template.html', {'travel_data': travel_data})


from django.shortcuts import render
import pandas as pd

def show_selected_spot(request, selected_index):
    # Fetch data from MySQL tables
    selected_spot_main = TourMain.objects.get(pk=selected_index)
    selected_spot_info = TourInfo.objects.get(tour=selected_spot_main)
    selected_spot_period = TourPeriod.objects.get(tour=selected_spot_main)
    selected_spot_etc = TourEtc.objects.get(tour=selected_spot_main)
    
    # Load the Excel file into a pandas DataFrame
    excel_file_path = '/home/lab09/MoodTrip/Top20_ImgList.xlsx'  # Update with your actual file path
    df = pd.read_excel(excel_file_path)

    # Filter the DataFrame to get image paths corresponding to the selected spot
    image_paths = df[df['tour_id'] == selected_index]['img_path'].tolist()

    # Extract filename from each image path
    image_names = [image_path.split('/')[-1] for image_path in image_paths]

    # Pass the fetched data to the template
    return render(request, 'Moodmatcher/selected_spot.html', {
        'selected_spot_main': selected_spot_main,
        'selected_spot_info': selected_spot_info,
        'selected_spot_period': selected_spot_period,
        'selected_spot_etc': selected_spot_etc,
        'image_names': image_names,
    })


def get_image_paths(spot_index):
    # 이미지 경로를 저장할 리스트
    image_paths = []

    # 엑셀 파일에서 이미지 경로 가져오기
    excel_file_path = "C:\\Users\\김현\\Desktop\\MoodTrip\\tourist_image_path.xlsx"
    df = pd.read_excel(excel_file_path)
    
    # 해당 spot_index에 해당하는 이미지 경로 가져오기
    for index, row in df.iterrows():
        if row['index1'] == spot_index:
            # 이미지 경로가 리스트 안에 있는 형식이므로 eval 함수를 사용하여 리스트로 변환
            image_paths.extend(eval(row['image_path']))
    
    return image_paths

## db data 불러오기 확인
from .models import TourCategory
from django.core.serializers import serialize

def tour_category(request, *args, **kwargs):
    tour_category_list = TourCategory.objects.all()
    json_data = serialize('json', tour_category_list)
    return JsonResponse(json_data, safe=False)
