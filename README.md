hitchhike memories
============================

## Requirements
- hugo v0.54.0
- yarn 1.13.0
- firebase-tools 6.3.0

## First
- `hugo`

```
brew install hugo
```

- `yarn`

```
brew install yarn
```

- `firebase-tools`

```
yarn global add firebase-tools
```


## Devlopment
- `http://localhost:1313`

```
hugo server -D -w
```

- `http://localhost:5000`

```
firebase serve
```

## Deploy
- Hosting to Firebase

```
firebase deploy
```

## Domain
https://htlp.work // TODO


## Add Photos
1. add photos to `others/hitchhike`
2. exec `new_post.py`

```
python new_post.py
```

3. Optionally adjust image rotation



## Reference
- https://gohugo.io/
- https://github.com/aerohub/phugo
