from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "diary" DROP CONSTRAINT IF EXISTS "fk_diary_user_4a190072";
        ALTER TABLE "diary" RENAME COLUMN "owner_id" TO "user_id";
        ALTER TABLE "userquestion" ADD "category" VARCHAR(50);
        ALTER TABLE "question" ADD "category" VARCHAR(50);
        ALTER TABLE "question" RENAME COLUMN "question_text" TO "content";
        ALTER TABLE "diary" ADD CONSTRAINT "fk_diary_user_9023c106" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "diary" DROP CONSTRAINT IF EXISTS "fk_diary_user_9023c106";
        ALTER TABLE "diary" RENAME COLUMN "user_id" TO "owner_id";
        ALTER TABLE "question" RENAME COLUMN "content" TO "question_text";
        ALTER TABLE "question" DROP COLUMN "category";
        ALTER TABLE "userquestion" DROP COLUMN "category";
        ALTER TABLE "diary" ADD CONSTRAINT "fk_diary_user_4a190072" FOREIGN KEY ("owner_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


MODELS_STATE = (
    "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"
)
