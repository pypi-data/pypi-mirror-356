from typing import Literal, Optional, TypedDict

TTSAudioEncoding = Literal[
    "AUDIO_ENCODING_UNSPECIFIED",
    "LINEAR16",
    "MP3",
    "OGG_OPUS",
]

TTSLanguageCodes = Literal["en-US", "ja-JP", "ko-KR", "zh-CN"]

TTSModelIds = Literal["v2", "v3"]

TTSVoices = Literal[
    "Agnes",
    "Alex",
    "Amanda",
    "Aoi",
    "Ashley",
    "Austin",
    "Bobbie",
    "Brandon",
    "Brett",
    "Brittany",
    "Caleb",
    "Casey",
    "Christopher",
    "Cody",
    "Craig",
    "Dawn",
    "Deborah",
    "Dennis",
    "Dohyun",
    "Dongmei",
    "Donna",
    "Douglas",
    "Dylan",
    "Edward",
    "Elizabeth",
    "Emily",
    "Emma",
    "Ethan",
    "Gregory",
    "Guocheng",
    "Hades",
    "Haruto",
    "Heather",
    "Hua",
    "Jennifer",
    "Jessica",
    "Jiho",
    "Jing",
    "Jisoo",
    "Joonhyuk",
    "Jordan",
    "Julia",
    "Julie",
    "Junyan",
    "Justin",
    "Kimberly",
    "Kristen",
    "Kyle",
    "Lei",
    "Lina",
    "Ling",
    "Logan",
    "Lori",
    "Malik",
    "Mark",
    "Mary",
    "Megan",
    "Michael",
    "Ming",
    "Minho",
    "Minji",
    "Nicole",
    "Olivia",
    "Philip",
    "Rachel",
    "Ronald",
    "Ryan",
    "Samantha",
    "Sarah",
    "Seojun",
    "Shaun",
    "Soojin",
    "Sunhao",
    "Taeyang",
    "Timothy",
    "Travis",
    "Tyler",
    "Wei",
    "Wendy",
    "William",
    "Xuan",
    "Yui",
    "Yuna",
    "Yuto",
]


class AudioConfig(TypedDict):
    audioEncoding: Optional[TTSAudioEncoding]
    speakingRate: Optional[float]
    sampleRateHertz: Optional[float]
    pitch: Optional[float]


class VoiceResponseMetadata(TypedDict):
    gender: Literal["VOICE_GENDER_UNSPECIFIED", "MALE", "FEMALE", "NEUTRAL"]
    age: Literal["VOICE_AGE_UNSPECIFIED", "CHILD", "TEEN", "ADULT", "SENIOR"]
    accent: Literal[
        "ACCENT_UNSPECIFIED",
        "ACCENT_BRITISH",
        "ACCENT_RUSSIAN",
        "ACCENT_AUSTRALIAN",
        "ACCENT_GERMAN",
        "ACCENT_FRENCH",
    ]


class VoiceResponse(TypedDict):
    languageCodes: list[TTSLanguageCodes]
    name: TTSVoices
    voiceMetadata: VoiceResponseMetadata
    naturalSampleRateHertz: int


class SynthesizeSpeechUsage(TypedDict):
    numProcessedCharacters: int
    modelId: TTSModelIds


class SynthesizeSpeechPhonemeTimingInfo(TypedDict):
    phoneme: str
    startTime: str


class SynthesizeSpeechResponse(TypedDict):
    audioContent: str
    numProcessedCharacters: int
    phonemeTimingInfo: Optional[SynthesizeSpeechPhonemeTimingInfo]
    usage: SynthesizeSpeechUsage
