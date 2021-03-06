#!/usr/bin/env python
# coding: utf-8


from pony.orm import *
from pony import orm
from datetime import datetime


mems = {
    'кот': [
        'https://mr-mem.ru/images/memes/mem-s-kotom-za-stolom.jpg',
        'https://i.pinimg.com/originals/db/20/3c/db203c1a9db65785b67551a15ccb9c1a.jpg',
        'https://static.boredpanda.com/blog/wp-content/uploads/2019/09/Heres-What-The-Cat-From-Woman-Yells-At-A-Cat-Meme-Looks-Like-In-Real-Life-5d725be9539e2__700.jpg',
        'https://cdn.ebaumsworld.com/2019/11/05/060250/86109023/womann-yelling-at-cat-1.jpg'
    ],
    'трамп': [
        'https://icdn.lenta.ru/images/2017/02/20/12/20170220122142227/pic_29a8244b69d74867b630447e64d93992.jpg',
        'https://junkee.com/wp-content/uploads/2020/11/count.jpg',
        'https://images.axios.com/sTneXyA-JXK6aGTWrKLc4sUiixY=/0x150:5472x3228/1920x1080/2021/01/08/1610064799740.jpg',
        'https://i.kym-cdn.com/entries/icons/original/000/031/249/thunberg.jpg',
        'https://i.ytimg.com/vi/Wl959QnD3lM/maxresdefault.jpg'
        
    ],
    'путин': [
        'https://i.ytimg.com/vi/oqEurDxUzqM/mqdefault.jpg',
        'https://memepedia.ru/wp-content/uploads/2020/06/shirokij-putin.jpg',
        'https://preview.redd.it/5xhbxd23u8s31.jpg?auto=webp&s=7232a43c94f588871e58b1bab33ae13806db2b03',
        'https://i.pinimg.com/originals/d2/8c/9a/d28c9a3fe7d91834d4959c1ece050b47.jpg'
    ],
    'random': [
        'https://i.redd.it/e2ilh7ik4el61.jpg',
        'https://i.redd.it/xjwnfagrmcl61.png',
        'https://i.redd.it/a8ln26mixcl61.jpg',
        'https://i.redd.it/crb4pgph1dl61.png',
        'https://i.redd.it/1bnm82i7fbl61.jpg',
        'https://i.redd.it/a6zsesiyddl61.jpg',
        'https://i.redd.it/6azs4lyu4dl61.png',
        'https://i.redd.it/8cysvc1xjdl61.jpg',
        'https://i.redd.it/jzkhiu5z4el61.jpg',
        'https://i.redd.it/8d6ehlkvcdl61.png',
        'https://i.redd.it/oij568p9rdl61.jpg',
        'https://i.redd.it/pmsviyw4dbl61.jpg',
        'https://i.redd.it/hqv582bylbl61.jpg',
        'https://i.redd.it/ozs44ao9ebl61.jpg',
        'https://i.redd.it/z8qhol2lqbl61.jpg',
        'https://i.redd.it/bvk8mhf8fbl61.jpg',
        'https://i.redd.it/667ljzs6wbl61.png',
        'https://i.redd.it/7ni7nfwwbcl61.jpg',
        'https://i.redd.it/fko5t36budl61.jpg',
        'https://i.redd.it/qu7g4wjxobl61.jpg',
        'https://i.redd.it/sv6kz2f5ral61.jpg',
        'https://i.redd.it/veyjtd7mjal61.jpg',
        'https://i.redd.it/iz08dkz7wal61.jpg',
        'https://i.redd.it/703b2chnrbl61.png',
        'https://i.redd.it/o9x73bmsjal61.jpg',
        'https://i.redd.it/7ak81ibxfel61.jpg',
        'https://i.redd.it/xqwtmt7uedl61.jpg',
        'https://i.redd.it/cbm38ogjncl61.jpg',
        'https://i.redd.it/u6wjcyxk5al61.jpg',
        'https://i.redd.it/6limivpinal61.jpg',
        'https://i.redd.it/f0s64s4jfel61.jpg',
        'https://i.redd.it/ir05lozrbal61.jpg',
        'https://i.redd.it/gj0do2zpkdl61.jpg',
        'https://i.redd.it/t9qjjnip3el61.png',
        'https://i.redd.it/aqbu2it7r9l61.jpg',
        'https://i.redd.it/shkzr1bu4al61.jpg',
        'https://i.redd.it/xtt575x85bl61.jpg',
        'https://i.redd.it/0lschtzb7bl61.jpg',
        'https://i.redd.it/666guow5rdl61.jpg',
        'https://i.redd.it/9a08a6ycnal61.jpg',
        'https://i.redd.it/jtzaxifky8l61.jpg',
        'https://i.redd.it/w11y8wbvy9l61.jpg',
        'https://i.redd.it/6a9lp2yaeel61.jpg',
        'https://i.redd.it/rgwnzgwe5al61.jpg',
        'https://i.redd.it/o3ug5ub2idl61.jpg',
        'https://i.redd.it/m0ckktkj6bl61.jpg',
        'https://i.redd.it/1qjtx9n7ydl61.jpg',
        'https://i.redd.it/knyk53il7dl61.jpg',
        'https://i.redd.it/eenk4hy39dl61.jpg',
        'https://i.redd.it/842ilzkrnal61.jpg',
        'https://i.redd.it/jv1jppx2q8l61.jpg',
        'https://i.redd.it/qn2o9xczr8l61.jpg',
        'https://i.redd.it/zlws74dvq9l61.jpg',
        'https://i.redd.it/7wdfxlmzzdl61.jpg',
        'https://i.redd.it/pwldneur59l61.jpg',
        'https://i.redd.it/fziof30do9l61.jpg',
        'https://i.redd.it/tvpzrfqh89l61.jpg',
        'https://i.redd.it/52zy96nvlel61.png',
        'https://i.redd.it/sme3jimundl61.jpg',
        'https://i.redd.it/5ui2v29658l61.jpg',
        'https://i.redd.it/ddvpyraikcl61.jpg'
    ]
}

music = {
    'морген': [
        'https://open.spotify.com/track/4KfmruShP5zOi9hYjM76e6?si=lE3o1gbgRqGrttn-JKgFxA',
        'https://open.spotify.com/track/2E5NGLtMqDmeijWcntP8Ca?si=Sk4P8WAeTL-93oNbuNYkCA',
        'https://open.spotify.com/track/6qWaZ2KzYhyrv1ILuAcIIv?si=F4VdGNF6Qcikb0NAP6pJAQ',
        'https://open.spotify.com/track/4EAiPdDayHEaYo3YKgbV7q?si=qDG9LKfoSLeP5Sy28HzxDQ',
        'https://open.spotify.com/track/272fe0z4cll7gJM3G8HFA8?si=gBD5mGZCSHeVqiRd0yqv2Q',
        'https://open.spotify.com/track/2vuRLuYUWwwQgQtg1TzkKj?si=siEF0TwITp6vDCBdnxBSZg',
        'https://open.spotify.com/track/0eou4g499YFO8jSxYQjvFH?si=wAzHKd7CRN-2MUws_IEpjQ',
        'https://open.spotify.com/track/7aCtjju6kQ316xn95FIOGq?si=W9Ga-G-kRyOYBT-546kVdA',
        'https://open.spotify.com/track/40XC3Fre6dJ2JzmYKsKhUU?si=dDz5TABvQXq3bX-7Rnt11A',
        'https://open.spotify.com/track/6faqUBsaHyt20aFqB6LPl0?si=2tnBdUNlRpSxWjWapHmohg',
        'https://open.spotify.com/track/3AsEkzwXpc2RwgmMGun3n8?si=UeIDCp6kREyR2r5r5B__Bw',
        'https://open.spotify.com/track/798PEmmgszuhw246bu4rbJ?si=p3dd61DDSWKaDUWhtslG3w',
        'https://open.spotify.com/track/0TNDUjDRK9QWj2YOM72eGV?si=XGlIJCmbSxWSrjxcz6__bA',
        'https://open.spotify.com/track/3Btd8g0SoeI0cbCXFZtEhP?si=rVK9_z2nQWOt0XVmvxW5zA',
        'https://open.spotify.com/track/1IcH4Z1Rz2gW4NXidENpuA?si=lxarZAhVSQGZJKCaRD7QKQ',
        'https://open.spotify.com/track/6WrOk13Whvdyvo6Kg5T8NY?si=E0GrVJrwQDOKA95YP6ut6Q',
        'https://open.spotify.com/track/4AfePQzDiboxwGnKN1TtkG?si=lYIi9MMETxilcguth1i-_Q',
        'https://open.spotify.com/track/409v3NsbudRh5QpXk2VKjo?si=zhfWJyOBT-Stry1s71MCUw',
        'https://open.spotify.com/track/6oHlAtmOkmEj0ciXZw1Fkk?si=fVzjhI2iQy6uUVuNLcDXrg',
        'https://open.spotify.com/track/4fPaYlUa2PprhS0AEa6A9n?si=jc2_FZDUQniqN6U-MwOCKA',
        'https://open.spotify.com/track/24OPKdtiI2NGNhXE3mBfUm?si=Ud-UxnzpSUO73AL3rR0Uww',
        'https://open.spotify.com/track/2OHtlG0qUAHhy9YLfDEo0K?si=jESVFNhqSO60NpsufMHXCw'
    ],
    'топ_россии': [
        'https://open.spotify.com/playlist/37i9dQZF1DX12G1GAEuIuj?si=EOdOxuzZQQaHQt9RcvAdSg'
    ],
    'big_baby_tape': [
        'https://open.spotify.com/track/5qhdXxsc1l7hQHOc1aZaGn?si=gtB93W4LRcmQWX0l9ljWYQ',
        'https://open.spotify.com/track/57rD7XtoxxJm229FITm556?si=HI8LEQ44QfSQLvqcjMfDrg',
        'https://open.spotify.com/track/15epnOVXX9PRB7A6z3YtZV?si=EM21Q4PmQwKDzF4RC3Bp9w',
        'https://open.spotify.com/track/1fkuCuWT3kJCJVqlQKHXNB?si=GrjUpZGDRNKQog0R8PY5kQ',
        'https://open.spotify.com/track/5EXJH0gMpIO54T1SSlDOcL?si=cI8xty25Q0ioPkQu7dLIlQ',
        'https://open.spotify.com/track/74yMuZVZTMh8btLb29gJlO?si=Qw2hB-5kR0iFRdY5wb1sKg',
        'https://open.spotify.com/track/2lHPJ1Fz3WPVp42tbulJcT?si=Pv4ZontPTeiZlBXH7nWJJQ',
        'https://open.spotify.com/track/2rm62qKHypKA2bqDO3Rja4?si=I4tmkTFtQaykl4XwqgkWVg',
        'https://open.spotify.com/track/7lZ52pdR0EoeHUI2H30Sn3?si=FuCnlC-7TAK-CffOOe7Gig',
        'https://open.spotify.com/track/4TPMVXdbaHe2bK9BEJX9xt?si=hlNglNtARqS4oAbdzCzPuA',
        'https://open.spotify.com/track/43RNYoUK2FpAnCQ81y5yJb?si=EPJJk4bTRnGcVce194w9_Q',
        'https://open.spotify.com/track/1sPiVQ1bYTfSp75gBJD3EX?si=q9N8b4tuQlyh23-tmueFmw',
        'https://open.spotify.com/track/2FY1IlminwSFudBXSx2fbR?si=p4hVFxOKRWOq8v9ql4F6gw',
        'https://open.spotify.com/track/6nxFOWUolqiK1prjDDRqV7?si=Vf7zt3PGRaSsebkScz79Ag',
        'https://open.spotify.com/track/7coGlyeuNyfc39Xfp3f1YM?si=inQE2Hz0RtK_7nOz81CR7g',
        'https://open.spotify.com/track/4fKyKyaQTDXLyvEusgRS0a?si=Bwihnq6xQTSa4Y9GbLk8HA',
        'https://open.spotify.com/track/2NryvrKN55a0leQvD2EdUQ?si=CAuQNSJ1QGy3WCrQJeGACQ',
        'https://open.spotify.com/track/3WSBOiXdV09RjUoy5weP1Y?si=qkcPV1j0RVabbZcNoiG2WQ',
        'https://open.spotify.com/track/5aS1IQpcM71wagQObbEYny?si=FLyLwafuTfCWPiEXaD6rYw',
        'https://open.spotify.com/track/3AzvXe83DmalUbAtJyQ2VQ?si=tYcWaZruRQ-cKQ23eAHoXQ',
        'https://open.spotify.com/track/4HEicTJ4HkDFiaFF7pJbVW?si=spnRmAPzSxGd9oqysMmsoA',
        'https://open.spotify.com/track/5NlUfFPL2z3RWAXy8NcRs8?si=hgMYZdwWRmWImEKLw8vgUQ',
        'https://open.spotify.com/track/2UhxaoPKEswNzdyacYr4jb?si=oY9gcfq9TYKOJFMYD3ekkQ',
        'https://open.spotify.com/track/2gbFfZbNkhF0Mym9q2aiEl?si=GfLSomeQT5--JEOoDVp6dA'
    ],
    'linkin_park': [
        'https://open.spotify.com/track/60a0Rd6pjrkxjPbaKzXjfq?si=bdKkcHEoSXWCh7Llfed7vA',
        'https://open.spotify.com/track/2nLtzopw4rPReszdYBJU6h?si=t1MThhSGQ4OMuOfTMRBUJw',
        'https://open.spotify.com/track/18lR4BzEs7e3qzc0KVkTpU?si=o28DTviXT_erWrr-OKxLig',
        'https://open.spotify.com/track/3K4HG9evC7dg3N0R9cYqk4?si=gopNbdw4RgyoEn199BS3MQ',
        'https://open.spotify.com/track/7oVEtyuv9NBmnytsCIsY5I?si=QNK4Y59_T5CtZZIbAW5Law',
        'https://open.spotify.com/track/0UFDKFqW2oGspYeYqo9wjA?si=MkcFB_UcQxKMQn21qqkTbA',
        'https://open.spotify.com/track/57BrRMwf9LrcmuOsyGilwr?si=iD6bNrQ4Q3KJJtV7g-3rhg',
        'https://open.spotify.com/track/3xXBsjrbG1xQIm1xv1cKOt?si=Aw9WVSCCSmCQcCSigewhGg',
        'https://open.spotify.com/track/1r1fPuhj9H4VdXr7OK6FL5?si=YxhcPy2eSxCjrJZKA-fQlg',
        'https://open.spotify.com/track/104buTcnP2AsxqB7U1FIZ4?si=pZdaXfyWQKewIWnn8Xknkw',
        'https://open.spotify.com/track/400lQTCx3wYGgqAIHSZbNA?si=NMW1FbAzSf6KJyC5IhtEwg',
        'https://open.spotify.com/track/2yss0n7KmvmSr4EHvjfFpn?si=UtZtXz_8RDWUg4aO69RGvw',
        'https://open.spotify.com/track/3fjmSxt0PskST13CSdBUFx?si=QeqZH5wQQkiEhQ1z1GSJYg',
        'https://open.spotify.com/track/4qVR3CF8FuFvHN4L6vXlB1?si=70mOWQ7SQkKXhvWhXZEnVw',
        'https://open.spotify.com/track/4wHktoSf6C0C0fAO8IIWqs?si=Vf0N86cpRemjzUMR7WT6ew',
        'https://open.spotify.com/track/32fEW4jygJjjnZh2iBa5IR?si=3_WWLnpOQw-krx0-EV7HvA',
        'https://open.spotify.com/track/7AB0cUXnzuSlAnyHOqmrZr?si=EHym4jboRFWiOsXACCm-yQ',
        'https://open.spotify.com/track/0rPTPahzhGx9LSzI8XX5OM?si=QcA570daRYqiMkFUlxUIcg',
        'https://open.spotify.com/track/3dxiWIBVJRlqh9xk144rf4?si=I7TK52mVTqukb8cZ-EpTjg',
        'https://open.spotify.com/track/697M5JB8FDIyRXEXgl1pBZ?si=rUqukYRvS42yjWZ58WjrQA',
        'https://open.spotify.com/track/1EU3VuKGZOvd1HTkxLPUXK?si=sUvjnQobTn-9XtwXdC2xPA',
        'https://open.spotify.com/track/00VKR5XH5jid1AgUdFz4bs?si=Tb7eujK0QQ6fO7hHOBN8Uw'
    ],
    'ariana_grande': [
        'https://open.spotify.com/track/1hG4V53eR16jg7jVTNLOiX?si=7e0UK8EeR2SK6FWGZQaLKg',
        'https://open.spotify.com/track/3DFnLXa69NVlOjbhTbXXNn?si=ZIfrpDKgSEeENo4g6UgJQA',
        'https://open.spotify.com/track/6ocbgoVGwYJhOv1GgI9NsF?si=1UT5homDTayYQirxv03zbw',
        'https://open.spotify.com/track/3e9HZxeyfWwjeyPAMmWSSQ?si=VeyhYdE2Q7W8VG5TSVDaQA',
        'https://open.spotify.com/track/4kV4N9D1iKVxx1KLvtTpjS?si=a9UanikXSvGyrGpHExvGlA',
        'https://open.spotify.com/track/5OCJzvD7sykQEKHH7qAC3C?si=SeFemkHEQEGV42ij4hP1ng',
        'https://open.spotify.com/track/3nef5W8jTkXrOKgCu4kmq7?si=ZOkrr6QVTGW5eOWnykE92g'
    ],
    'the_weeknd': [
        'https://open.spotify.com/track/5QO79kh1waicV47BqGRL3g?si=dXI8D5bUTsikrBKfE11WOQ',
        'https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b?si=ZCPYexuQRmCM4meCDyI_dw',
        'https://open.spotify.com/track/7fBv7CLKzipRk6EC6TWHOB?si=r7OXpsg_TleHaz6kVN4fkg',
        'https://open.spotify.com/track/7szuecWAPwGoV1e5vGu8tl?si=99WssNsWTJu1DJ4C8D2vDQ',
        'https://open.spotify.com/track/7MXVkk9YMctZqd1Srtv4MB?si=_5S1Rl35STGbXFSXS5jRjg',
        'https://open.spotify.com/track/5GXAXm5YOmYT0kL5jHvYBt?si=1V9ewAlUQliTDH5JUAMGAQ',
        'https://open.spotify.com/track/22VdIZQfgXJea34mQxlt81?si=mwzAm864QY2QU0jujD5JkQ',
        'https://open.spotify.com/track/4oeaIftdpT3JuZLcCkKmVE?si=PVEH0djWRPyA8pMD2R5Ayg'
    ],
    'justin_timberlake': [
        'https://open.spotify.com/track/4rHZZAmHpZrA3iH5zx8frV?si=_G7xh3-VTmm45O4NhpX1Dg',
        'https://open.spotify.com/track/0O45fw2L5vsWpdsOdXwNAR?si=yMUaHDXpQs6XsW1y972rGA',
        'https://open.spotify.com/track/6JV2JOEocMgcZxYSZelKcc?si=e8S9Bp1STNmMbEIs9K_Gxg',
        'https://open.spotify.com/track/7Lf7oSEVdzZqTA0kEDSlS5?si=3LTPUvZQRaufsgMs02qUwQ',
        'https://open.spotify.com/track/1LhMopPAallLeaeNutqbgS?si=IEQvyBzzTc-02CeunR-Ovg',
        'https://open.spotify.com/track/5GrXtQYnHaS8UE4rXDqyO0?si=PihYjS3JQL-nYpmpm_vuSA',
        'https://open.spotify.com/track/4KTU5aa5s547f1JF5DImhF?si=yq2CapXITCOVCIdTcuvJSg',
        'https://open.spotify.com/track/3qYCfox9txQoEQAG0mbwd5?si=wRWMneZeQZG6dxAX7XszgA',
        'https://open.spotify.com/track/4ZrEjG3Vef85NTve8ptC9Q?si=jHW-6EviRdCoi2QuQH4ElQ',
        'https://open.spotify.com/track/1MBM7CyZbwJpVbbZJnHHRg?si=kHiUK8BXTF6REJabYGFo6w'
    ],
    'eminem': [
        'https://open.spotify.com/track/7FIWs0pqAYbP91WWM0vlTQ?si=K3dfzDBVT6CVNd5ann8KDQ',
        'https://open.spotify.com/track/4xkOaSrkexMciUUogZKVTS?si=M6Td4mjPQ3mr6ydI8X9VQQ',
        'https://open.spotify.com/track/7lQ8MOhq6IN2w8EYcFNSUk?si=BL0fs1MCRAmQeBvDsj1i-Q',
        'https://open.spotify.com/track/15JINEqzVMv3SvJTAXAKED?si=RmwEpaz_QmS_QR-0HpBiYw',
        'https://open.spotify.com/track/3yfqSUWxFvZELEM4PmlwIR?si=bpZFLIb6QAmKV0663k9qgw',
        'https://open.spotify.com/track/7Ie9W94M7OjPoZVV216Xus?si=6royyn19Q_CDU3TxOZ6u3Q',
        'https://open.spotify.com/track/3UmaczJpikHgJFyBTAJVoz?si=NBfUmKIUT_i_-G4D3MhCuw',
        'https://open.spotify.com/track/6cS9PmLky2NhLOhpIsUlow?si=goQNvNOiSOam2hN2K0Dd9w',
        'https://open.spotify.com/track/6or1bKJiZ06IlK0vFvY75k?si=G_0qTWmCQYW5VG5soFnLmQ',
        'https://open.spotify.com/track/1v7L65Lzy0j0vdpRjJewt1?si=pN8usaLORiaLM6U8v-kjcA',
        'https://open.spotify.com/track/2gsNpSn7VvvJuSrIDfRoYy?si=Ll3_8V4BTWqcOcz6TY80vg',
        'https://open.spotify.com/track/2SL6oP2YAEQbqsrkOzRGO4?si=l-PmipcsTweV-LGrqyWWgA',
        'https://open.spotify.com/track/28FGV3ORH14MYORd7s5dlU?si=OJzx7M2CSJaOPC7lo3mqRA',
        'https://open.spotify.com/track/2XTquzYQAdT1Hk78bOUwsv?si=DlrAs33QRHyqTWDeewM2hQ',
        'https://open.spotify.com/track/4UTpObwAYO67yymOoCeXwS?si=RNfnqW0VTPWRQVpbVnJwrw',
        'https://open.spotify.com/track/6Xk7PnitV9jCRorWt2LiVZ?si=mvI_2yM4TySx7l5Nq4r-Qw',
        'https://open.spotify.com/track/4WgvTITBJbEfCJHguiE7QS?si=vkQo0w_3RnOK8IQpbmejsQ',
        'https://open.spotify.com/track/0qcjuYtMWhBjXg0Xwt5SzS?si=VdhMyTKMTT-3WQT5FTgQ6A',
        'https://open.spotify.com/track/4gXdMZkBN1neE9nX6yRALa?si=A3o2h3A9T8eug8kqg09img',
        'https://open.spotify.com/track/4woTEX1wYOTGDqNXuavlRC?si=OEX_FnQKQMaZR26wFQe1Ow'
    ],
    'juice_wrld': [
        'https://open.spotify.com/track/285pBltuF7vW8TeWk8hdRR?si=Aek79LDiQo2CGulaKGj40A',
        'https://open.spotify.com/track/6Hj9jySrnFppAI0sEMCZpJ?si=N-acQ6lKTra52WbdkVXDPQ',
        'https://open.spotify.com/track/4VXIryQMWpIdGgYR4TrjT1?si=WDthSTS6QveqIMAbSVHn1g',
        'https://open.spotify.com/track/5dOxHHMOFAbG3VH23t0xNm?si=UlpspXNMQmyMVwoLxo1VPg',
        'https://open.spotify.com/track/4K06PO78fW4mnBVenxGNob?si=73mqKIiXRBWdCeU4rKUDZg',
        'https://open.spotify.com/track/6wQlQrTY5mVS8EGaFZVwVF?si=49eZ1UagQG6ouTPoI49_yg',
        'https://open.spotify.com/track/0440JCJyIAmINA8KcYgFb5?si=UgK--StVSj6luK5LRLWwng',
        'https://open.spotify.com/track/4F6YLjakjqWFTgC5qfEwPQ?si=l8nGXoHXTjSCBzPkvF7E_w',
        'https://open.spotify.com/track/7pbg3ABlAZv2NiIdKbBBFm?si=Dx_w9rIwSgGr5kl4pLZ_bA',
        'https://open.spotify.com/track/21CkzgKCBCq5V4XKjiGSIj?si=OkQgIXIRSv-lmTYsHRzXvA',
        'https://open.spotify.com/track/4PPLJAEYBSOcnzr9TZoqf9?si=uV7Oe66mTDmyE77wvvnnEA',
        'https://open.spotify.com/track/7AvprzMsRJpybaalckaT8c?si=nH-8KBDJTyaw2lhIGNQEPA'
    ],
    'post_malone': [
        'https://open.spotify.com/track/21jGcNKet2qwijlDFuPiPb?si=ea_bFKKMQ-usnyYm1gbqug',
        'https://open.spotify.com/track/0e7ipj03S05BNilyu5bRzt?si=c8AxfuA2SkmHjGc2EzRPbw',
        'https://open.spotify.com/track/0RiRZpuVRbi7oqRdSMwhQY?si=S2jgigFxS2OR-nubC0rpSA',
        'https://open.spotify.com/track/7dt6x5M1jzdTEt8oCbisTK?si=juKLAfqWR12VYhtlhPAIEg',
        'https://open.spotify.com/track/7xQAfvXzm3AkraOtGPWIZg?si=iSN7jtoUR-ysVbIiu0-5hA',
        'https://open.spotify.com/track/3a1lNhkSLSkpJE4MSHpDu9?si=XEoh6tC1SmKKTrbZDep6qQ',
        'https://open.spotify.com/track/0t3ZvGKlmYmVsDzBJAXK8C?si=2X5GeQxrRkaV7gs101CBew'
    ],
    'lil_peep': [
        'https://open.spotify.com/track/30bqVoKjX479ab90a8Pafp?si=6IaCzISjSZWlmgGjhcHDDQ',
        'https://open.spotify.com/track/4jvjzW7Hm0yK4LvvE0Paz9?si=h2e3BHK_R9G6OE30U2bpzw',
        'https://open.spotify.com/track/0S0vWvyZ6Rc79TXkWxT9QA?si=lpTDBqucRVmQ3jHPi3eKWA',
        'https://open.spotify.com/track/7hf89cT5FEmLV5E9fjrjG7?si=kM6GGFMWQW6wbEQQj6Yitw',
        'https://open.spotify.com/track/1Z8gpnzgTFQKAwmV43iLBB?si=lNdgjtlySUCabWhtHkW_vw',
        'https://open.spotify.com/track/3kBD2xHIqKWXjLAGidDTSz?si=Ze02QJ6fQYCuwBEhiT5LLw',
        'https://open.spotify.com/track/6VrCmhRBFnuGKmtNfk4jDs?si=yL8i8F_iRCq8r1F5YwHJ6A',
        'https://open.spotify.com/track/2D27mEHstGhdGONAhcEU6q?si=i9Z4n-zQT3OE7WcGYSSrzA',
        'https://open.spotify.com/track/7kjYPapOatvPuqPuMn4TgM?si=wl_6wRUWTmiwiMgDib9Utw',
        'https://open.spotify.com/track/7yGRdlRrscxNhHsMS5HPAM?si=UYcrBMJ0TPq20Nzxh7gYCg'
    ],
    'joji': [
        'https://open.spotify.com/album/5EzDhyNZuO7kuaABHwbBKX?si=gtM5T43iQi2jyNrOa7hHdQ'
    ],
    'макс_корж': [
        'https://open.spotify.com/track/14JceK2UBLd0UUm23N5lRy?si=e21amAu0RP-ecW6ynRj8vw',
        'https://open.spotify.com/track/5kz9d0Cxx7RK8PjRLlWnAt?si=7psQYuCqTtiYVGVl1qw6tw',
        'https://open.spotify.com/track/4BzDIOl9JXFhjglnAxvUCz?si=yAGivwVcTTWUHgJ3Wq0dkg',
        'https://open.spotify.com/track/7f6ALwMTMLAhXCfoHYLCsx?si=U5HsklWwRh6jxL_-jdAAvg',
        'https://open.spotify.com/track/2fP2RBX81C55kEBaHZHomY?si=gXVolKdIQbC-7K8KgO_-Cg',
        'https://open.spotify.com/track/06jEcxzahUi9GdN5RFsqO4?si=-FAYsXMFTLWZcOr24YL1SA'
    ],
    'random': [
        'https://open.spotify.com/track/5P7FwhkLQp2HrfR79pYDj5?si=8PVRJg7CSmuiSpbOZsBVqA',
        'https://open.spotify.com/track/21A3Yv2ifXxtoM03Sc0IDM?si=ajeZDQtQROOXiH7Lu6IvnA',
        'https://open.spotify.com/track/7ikRId3U9AXd6tfF2fbItC?si=O3IicJBFRwOT5vDdPk5wKA',
        'https://open.spotify.com/track/6zFMeegAMYQo0mt8rXtrli?si=SHxaGa-OQV2w-K95MTWWfw',
        'https://open.spotify.com/track/0F7FA14euOIX8KcbEturGH?si=nwgupapUSne-kqgQG-Z7Aw',
        'https://open.spotify.com/track/1000nHvUdawXuUHgBod4Wv?si=8ghW34EtQ3S9lR-ChB_MOA',
        'https://open.spotify.com/track/7bCfHiRcfUjG0YVVNUL7Ve?si=UJowR7VbRZapUwQfC2w0bA',
        'https://open.spotify.com/track/2zca6hOc4QDTJUuZ6THBCa?si=TO5IxcgDSXK46hU4YzY0Qg',
        'https://open.spotify.com/track/5A6OHHy73AR5tLxgTc98zz?si=YuVCF4pKS-e463RMSu_tkA',
        'https://open.spotify.com/track/6fujklziTHa8uoM5OQSfIo?si=gV6YI7pPRH65A-JMoaDgsQ',
        'https://open.spotify.com/track/6y6jbcPG4Yn3Du4moXaenr?si=tYdhIRuAQzquq2t63g7GtQ',
        'https://open.spotify.com/playlist/0vvXsWCC9xrXsKd4FyS8kM?si=HRxY1-bZTkWGuB68_7egrw',
        'https://open.spotify.com/track/7FyV5LIUxjyAFo51XK8g8z?si=BZ6hPno2QwulDRNyeUyLPw',
        'https://open.spotify.com/track/6tO5bxNnMuh1c3cziSpecA?si=lw0GGHF5ScusEQCOgwyNVg',
        'https://open.spotify.com/track/0kEZlJh4mK1QRfb3CT5LPk?si=lUW39ZDrRrW7Ukw1zermRA',
        'https://open.spotify.com/track/1tm7c4V0kqLiN0XPVnoUcT?si=1X8dZvSfSqOoWslwWxo9yw',
        'https://open.spotify.com/track/1GOiMxQXZUzjzH0Sxpck0B?si=xBA3O4a2T2WQCocWpGA2bA',
        'https://open.spotify.com/track/68rVGSTnCiFOET9k5Vd8Se?si=bJcRqTelQ7ClhqZ7SQihGw'
    ],
    'басс': [
        'https://open.spotify.com/playlist/3PmHkNHWu8l5uM8Xab5w6H?si=RZIPPW_6T7K6941ajpy5Ew'
    ],
}

commands = {
    # TODO
    'mem': '"help for mem"',
    'music': '"help for music"',
    'movie': '"help for movie"'
}

movies = {
    # TODO
    'website': [
        'https://www.kinopoisk.ru/',
        'https://www.ivi.ru/',
        'https://www.netflix.com/',
        'https://okko.tv/',
        'https://megogo.ru/ru'
    ]
}

play = {
    # TODO
    'text0': 'text in messange0',
    'play1': {
        'text1': 'text in messange1',
        'choice1': {
            'text2': 'text in messange2',
            'choice1.1': {
                'text3': 'text in messange3',
                'choice1.1.1': 'end1'
            },
            'choice1.2': 'end2'
        },
        'choice2': {
            'choice2.1': {
                'choice2.1.1': {
                    'choice2.1.1.1': 'end3',
                    'choice2.1.1.2': 'end4'
                },
                'choice2.1.2': {
                    '13': '14',
                    '15': '16'
                }
            },
            'choice2.2': 'end'
        },
        'choice3': '18'
    },
    'play2': {}
}


def parsing_rbc():
    # TODO
    pass


db = Database()


@db_session
class Mem(db.Entity):
    topic = Required(str)
    link = Required(str)
    date = Required(str)


@db_session
class Music(db.Entity):
    singer = Required(str)
    link = Required(str)
    date = Required(str)


@db_session
class Command(db.Entity):
    name = Required(str)
    help = Required(str)
    date = Required(str)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

db.generate_mapping(create_tables=True)

set_sql_debug(True)

links = set()
for topic in mems.keys():
    for link in mems[topic]:
        if link not in links:
            Mem(topic=topic, link=link, date=datetime.now().strftime("%d.%m.%y %H:%M:%S"))
            links.add(link)

links = set()
for singer in music.keys():
    for link in music[singer]:
        if link not in links:
            Music(singer=singer, link=link, date=datetime.now().strftime("%d.%m.%y %H:%M:%S"))
            links.add(link)

names = set()
for command in commands.keys():
    if command not in names:
        Command(name=command, help=commands[command], date=datetime.now().strftime("%d.%m.%y %H:%M:%S"))

commit()
