import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_helper
from core.models import User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print(f"user {user} created")
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print("Found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(
    session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    # users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # # users = result.unique().scalars()
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        for post in user.posts:
            print("***", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:
        print("post", post)
        print("author", post.user)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("***", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        # .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        ).order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        await get_profiles_with_users_and_users_with_posts(session=session)
        # await create_user(session=session, username="Mike")
        # await create_user(session=session, username="Alice")
        # await get_user_by_username(session=session, username="Sam")
        # user_Mona = await get_user_by_username(session=session, username="Mona")
        # user_Mike = await get_user_by_username(session=session, username="Mike")
        # # await create_user_profile(
        # #     session=session,
        # #     user_id=user_Mona.id,
        # #     first_name="Mona",
        # #     last_name="Bobova",
        # # )
        # # await show_users_with_profiles(session)
        # await create_posts(
        #     session,
        #     user_Mona.id,
        #     "SQLA 2.0",
        #     "SQLA Joins",
        # )
        # await create_posts(
        #     session,
        #     user_Mike.id,
        #     "FastAPI intro",
        #     "FastAPI Advanced",
        #     "FastAPI more",
        # )
        # await get_posts_with_authors(session=session)


if __name__ == "__main__":
    asyncio.run(main())
