import pytest
from authenticator import Authenticator

@pytest.fixture
def auth():
    authenticator = Authenticator()
    yield authenticator
 
# ユーザーが正しく登録されていることを確認するテスト
def test_register_user(auth):
    auth.register("user1", "password1")
    assert auth.users["user1"] == "password1"

# すでに存在するユーザー名で登録を試みた場合に、エラーメッセージが出力されるかを確認するテスト
def test_register_existing_user(auth):
    auth.register("user2", "password2")
    with pytest.raises(ValueError, match="ユーザーは既に存在します。"):
        auth.register("user2", "newpassword")

# 正しいユーザー名とパスワードでログインできるかを確認するテスト
def test_register_and_login(auth):
    auth.register("user1", "password1")
    assert auth.login("user1", "password1") == "ログイン成功"

# 誤ったパスワードでエラーが出るかを確認するテスト
def test_login_invalid_credentials(auth):
    auth.register("user3", "password3")
    with pytest.raises(ValueError, match="ユーザー名またはパスワードが正しくありません。"):
        auth.login("user3", "wrongpassword")
    with pytest.raises(ValueError, match="ユーザー名またはパスワードが正しくありません。"):
        auth.login("nonexistentuser", "password")
