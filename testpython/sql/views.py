from django.shortcuts import render
from django.db import connection
from django.db import IntegrityError
from django.shortcuts import redirect
from .models import Post, User
from django.utils.html import escape


# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         # 사용자 이름이 이미 존재하는지 확인
#         with connection.cursor() as cursor:
#             cursor.execute(f"SELECT username FROM sql_user WHERE username = '{username}'")
#             existing_user = cursor.fetchone()
#
#         if existing_user:
#             # 이미 존재하는 사용자 이름이라면 에러 메시지 표시
#             return render(request, 'register.html', {'error_message': '이미 존재하는 사용자 이름입니다.'})
#         else:
#             try:
#                 # 사용자 데이터를 저장
#                 sql_query = f"INSERT INTO sql_user (username, password, power) VALUES ('{username}', '{password}','1')"
#                 admin = f"INSERT INTO sql_user (username, password, power) VALUES ('admin', 'password', '0')"
#                 with connection.cursor() as cursor:
#                     cursor.execute(sql_query)
#                     cursor.execute(admin)
#
#                 return render(request, 'login.html')
#             except IntegrityError:
#                 # 데이터베이스 무결성 오류 처리
#                 return render(request, 'register.html', {'error_message': '회원가입 중 오류가 발생했습니다.'})
#
#     return render(request, 'register.html')
#
#
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         # # 안전하지 않은 코드
#         # # SQL 쿼리를 사용하여 사용자 인증을 시도
#         # sql_query = f"SELECT * FROM sql_user WHERE username = '{username}' AND password = '{password}'"
#         #
#         # # sql 쿼리문 실행
#         # with connection.cursor() as cursor:
#         #     cursor.execute(sql_query)
#         #     user = cursor.fetchone()
#
#         #특수기호 들어가있으면 오류
#         if any(char in username + password for char in
#                ['<', '>', '&', '"', "'", '/', '\\', '#', '{', '}', '%', '(', ')', '+']):
#             return render(request, 'login.html', {'error_message': '잘못된 접근입니다.'})
#         # 특수 기호 필터링
#         sql_query = "SELECT * FROM sql_user WHERE username = %s AND password = %s"
#         filtered_chars = ['<', '>', '&', '"', "'", '/', '\\', '#', '{', '}', '%', '(', ')', '+']
#         filtered_username = ''.join(char for char in username if char not in filtered_chars)
#         filtered_password = ''.join(char for char in password if char not in filtered_chars)
#         #
#         # 특수 기호 필터링
#         with connection.cursor() as cursor:
#             cursor.execute(sql_query, (filtered_username, filtered_password))
#             user = cursor.fetchone()
#         #사용자 인증
#             if user is not None:
#                 # 사용자 인증 성공
#                 response = redirect('notice')
#                 # power 배열은 3이다.
#                 if user[3] == '0':
#                     return redirect('/admin/')
#                 else:
#                     return response
#             else:
#                 # 사용자 인증 실패 처리
#                 return render(request, 'login.html', {'error_message': '사용자 정보가 다릅니다. 다시 로그인 해주세요.'})
#
#     return render(request, 'login.html')
#
# def logout(request):
#     # Clear the authentication cookie
#     response = redirect('login')
#     return response
#
# def notice(request): #게시판
#     # 모든 Post를 가져와 postlist에 저장
#     postlist = Post.objects.all()
#
#     if request.method == 'POST':
#         input = request.POST['input']
#         sql_query = f"SELECT * FROM sql_post WHERE id = '{input}'"
#
#         with connection.cursor() as cursor:
#             cursor.execute(sql_query)
#             num = cursor.fetchone()
#         if num is not None:
#             return redirect('/sql/notice/' + input + '/')
#
#     # notice.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옴
#     return render(request, 'notice.html', {'postlist': postlist})
#
#
# def noticeAdd(request): #게시글 작성
#     if request.method == 'POST':
#         postname = request.POST['postname']
#         contents = request.POST['contents']
#         username = request.user.username
#         sql_query = f"INSERT INTO sql_post (postname, contents, writer) VALUES ('{postname}', '{contents}','{username}')"
#         with connection.cursor() as cursor:
#             cursor.execute(sql_query)
#         return redirect('/sql/notice/')
#
#     return render(request, 'noticeAdd.html')
#
# def posting(request, pk): #게시글 포스팅
#     # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
#     post = Post.objects.get(pk=pk)
#
#     if request.method == 'POST': #게시글 삭제
#         post.delete()
#         return redirect('/sql/notice/')
#
#     # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
#     return render(request, 'posting.html', {'post':post})

# ---------------------------안전한 코드 ---------------------------------------#

def register(request): #회원가입 페이지
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        sql_query = "SELECT * FROM sql_user WHERE username = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql_query, (username,))
            user = cursor.fetchone() # DB 유저 확인

        if user is None:  # 유저가 있다면 생성실패
            # SQL 쿼리를 사용하여 사용자 데이터를 저장

            sql_query = "INSERT INTO sql_user (username, password, power) VALUES (%s, %s, '1')"

            with connection.cursor() as cursor:
                cursor.execute(sql_query, (username, password))

            return redirect('/sql/login/')
        else:
            # 사용자 가입 실패 처리
            return render(request, 'register.html', {'error_message': '계정이 이미 있습니다. 다시 가입 해주세요.'})



def login(request): #로그인 페이지
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']  # 입력 아이디
        password = request.POST['password']  # 입력 패스워드

        sql_query = f"SELECT * FROM sql_user WHERE username = %s" #DB 유저 확인
        with connection.cursor() as cursor:
            cursor.execute(sql_query, (username,))
            num = cursor.fetchone()
        if num is not None: #유저가 있다면
            user = User.objects.get(username=username) #DB에서 해당 유저 가져오기
            if (password == user.password):  # 비밀번호 대조
                request.session['user_id'] = user.id  # 일치할시 세션에 userDB id 가져오기
                if (user.power == '0'):
                    return redirect('/admin/')  # 권한자만 이동
                return redirect('/sql/notice/')  # 계시판 이동
        else:
            # 사용자 인증 실패 처리
            return render(request, 'login.html', {'error_message': '사용자 정보가 다릅니다. 다시 로그인 해주세요.'})


def logout(request):
    # 로그아웃은 session에 저장된 user_id을 지움
    if request.session.get('user_id'):
        del (request.session['user_id'])
    return redirect('/sql/login/')
def notice(request): #게시판
    user_id = request.session.get('user_id')
    if user_id: # 세션에 user가 존재한다면
        user = User.objects.get(pk=user_id)
        postlist = Post.objects.all()

        if request.method == 'POST': #게시글 포스팅
            input = request.POST['input']
            sql_query = f"SELECT * FROM sql_post WHERE id = '%s'"
            with connection.cursor() as cursor:
                cursor.execute(sql_query,(input))
                num = cursor.fetchone()
            if num is not None:
                return redirect('/sql/notice/' + input + '/')

        return render(request, 'notice.html', {'postlist': postlist , 'user': user})
    # 세션 끊길시
    else:
        redirect('/sql/login/')


def noticeAdd(request):
    user_id = request.session.get('user_id')

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        # Handle the case when the user is not logged in
        return redirect('login')  # Redirect to the login page or handle it in your way

    if request.method == 'POST':
        postname = request.POST['postname']
        contents = request.POST['contents']

        sql_query = "INSERT INTO sql_post (postname, contents, writer) VALUES (%s, %s, %s)"

        with connection.cursor() as cursor:
            cursor.execute(sql_query, (postname, contents, user.username))

        return redirect('/sql/notice/')

    return render(request, 'noticeAdd.html')

def posting(request, pk): #게시글 포스팅
    user_id = request.session.get('user_id')
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)

    if request.method == 'POST': #게시글 삭제
        post.delete()
        return redirect('/sql/notice/')

    # postname과 contents에 대한 이스케이핑을 적용하여 XSS 공격 방지
    filtered_chars = ['<', '>', '&', '"', "'", '/', '\\', '#', '{', '}', '%', '(', ')', '+', '']
    # 특수 문자를 re place 함수를 사용하여 필터링
    filtered_postname = post.postname
    filtered_contents = post.contents
    for char in filtered_chars:
        filtered_postname = filtered_postname.replace(char, '')
        filtered_contents = filtered_contents.replace(char, '')

    # 이스케이핑을 적용하여 안전한 문자열 생성
    safe_postname = escape(filtered_postname)
    safe_contents = escape(filtered_contents)

    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'posting.html', {'post': post, 'safe_postname': safe_postname, 'safe_contents': safe_contents})

