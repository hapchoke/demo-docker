
from django import forms

PREFECTURES = (
    (1, '北海道'),
    (2, '青森県'),
    (3, '岩手県'),
    (4, '宮城県'),
    (5, '秋田県'),
    (6, '山形県'),
    (7, '福島県'),
    (8, '茨城県'),
    (9, '栃木県'),
    (10, '群馬県'),
    (11, '埼玉県'),
    (12, '千葉県'),
    (13, '東京都'),
    (14, '神奈川県'),
    (15, '新潟県'),
    (16, '富山県'),
    (17, '石川県'),
    (18, '福井県'),
    (19, '山梨県'),
    (20, '長野県'),
    (21, '岐阜県'),
    (22, '静岡県'),
    (23, '愛知県'),
    (24, '三重県'),
    (25, '滋賀県'),
    (26, '京都府'),
    (27, '大阪府'),
    (28, '兵庫県'),
    (29, '奈良県'),
    (30, '和歌山県'),
    (31, '鳥取県'),
    (32, '島根県'),
    (33, '岡山県'),
    (34, '広島県'),
    (35, '山口県'),
    (36, '徳島県'),
    (37, '香川県'),
    (38, '愛媛県'),
    (39, '高知県'),
    (40, '福岡県'),
    (41, '佐賀県'),
    (42, '長崎県'),
    (43, '熊本県'),
    (44, '大分県'),
    (45, '宮崎県'),
    (46, '鹿児島県'),
    (47, '沖縄県'),
)

class CheckOutForm(forms.Form):
    zip=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control p-postal-code",
        'id':"zip",
         'name':'zip',
         'size':"8",
         'maxlength':"8",
    }),required=True)
    prefecture=forms.ChoiceField(widget=forms.Select(attrs={
        'class':'custom-select d-block w-100 p-region-id',
        'id':'prefecture',
        'name':'prefecture',
    }), choices=PREFECTURES, required=True)
    street_address=forms.CharField(widget=forms.TextInput(attrs={
        'id':"street_address",
        'name':'street_address',
        'class':"form-control p-locality p-street-address p-extended-address",
        'placeholder':"千代田区霞が関 2-1-6",
    }),required=True)
    apartment_address=forms.CharField(widget=forms.TextInput(attrs={
        'id':"apartment_address",
        'name':'apartment_address',
        'class':"form-control",
        'placeholder':"あさがお荘 202号室",
        
    }),required=False)
    default=forms.BooleanField(required=False)