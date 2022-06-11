# 솔트룩스 x 서울산업진흥원 : 인공지능 자연어처리 및 음성인식/음성합성 기술을 활용한 응용 SW 개발자 양성과정
# 프로젝트 이름 : Ai-AeSop
## 프로젝트 소개 
Ai-AeSop은 어린아이를 위한 동화 서비스입니다. 부모님의 목소리, 캐릭터의 목소리를 통해 동화를 읽어주는 서비스(TTS), 동화를 생성해보는 서비스, 문장을 통해 그림을 그려주는 서비스를 제공합니다.
## 동화 읽어주기
![image](https://user-images.githubusercontent.com/81752763/172761366-3beccf1f-2fef-4cdd-a1f1-8439a066bb48.png)
- 음성 데이터 수집 및 전처리
  - 실제 목소리 녹음, NAVER CLOVA 목소리 녹음(3900문장)
  - librosa를 활용한 전처리
- Glow-TTS
  - 플로우 기반 생성 모델
  - 텍스트 순서에 따라 발화를 차례대로 정렬
  - 매우 긴 텍스트를 빠르게 합성
  - 서로 다른 강세와 억양을 갖춘 발화를 생성
  - Tacotron 2와 비교해 비슷한 품질의 음성을 약 15배 빠르게 생성
  - 300 ~ 400 에폭(6시간) 학습
- HiFi-GAN
  - 음성 오디오의 주기적 신호를 구별해내는 방식의 HiFi-GAN을 보코더로 사용
  - Glow-TTS를 통해 생성된 Mel-spectrogram에서 waveform을 생성
  - 300 ~ 400 에폭(6시간) 학습
- g2pk
  - TTS모델에 들어가는 텍스트에 대한 전처리
  - 자소를 음소로 변환하는 작업
- 예시

https://user-images.githubusercontent.com/81752763/172762497-48deec20-a7d8-442e-afec-3cffb35c81a9.mp4


## 동화 생성하기
![image](https://user-images.githubusercontent.com/81752763/172761845-6605ed56-42cc-47f7-a5a0-b4dc7f0153b7.png)
- 데이터 수집 및 전처리
  - 영어 동화 데이터 91478문장
  - 기본 전처리
- GPT2 
  - Masked self attention 사용
- 예시

https://user-images.githubusercontent.com/81752763/172762622-335e5912-b5c3-4d68-9fa2-59727eb5d017.mp4


## 이미지 생성
- Glide
  - OpenAI 이미지 생성 모델 Glide 사용
  - DALL-E 2의 기본 구조
  - GAN이 주축이던 Text-to-image domain에 Diffusion model을 도입해 사실적인 이미지 생성
  ![image](https://user-images.githubusercontent.com/81752763/172762342-72792a4b-f5db-48f7-b565-be799e14e89d.png)

## 개선 방향
- 서버 환경에서 개발시 FastPitch 사용 고려
- 노이즈가 많은 데이터로 고품질의 TTS 모델 만들기
- 실제 동화를 읽어주는 말투, 어조 표현
- 한국어 데이터 확보 후 한국 동화 생성 서비스 
