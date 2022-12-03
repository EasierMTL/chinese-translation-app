# System Design

## UI

- `/`: Home Page
- `/demo`: Demo of Translator
  - Rate limit based on IP
- `/login`
- `/sign-up`
- `/sign-out`
- `/user/translate`: Actual Production Grade Translator

## API

Under `/api`

- `/auth`
  - `/login`
  - `/sign-up`
  - `/sign-out`
  - Support both UN/password and OAuth
- `/translate`
  - Translates whole text
  - Set a length limit in the editor
- `/translate-dict`
  - Translates with a Chinese Dictionary
    - Provides important information like pinyin, multiple meanings, usage
    - Use yabla's API (?)
