import timeit
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

iter_no = 5000
text1 = ""
text2 = ""

search1 = "Алгоритм Кнута-Морріса-Пратта"
search2 = "Алгоритм Боєра-Мура"
search3 = "Алгоритм Рабіна-Карпа"

with open("стаття 1.txt",'r',encoding="UTF-8") as fh:
    text1 = fh.read()
with open("стаття 2.txt",'r',encoding="UTF-8") as fh:
    text2 = fh.read()

pattern = "алг"
false_pattern = "asdffg"
t1_1 = timeit.timeit('kmp_search(text1, pattern)', globals=globals(),number=iter_no)
t1_2 = timeit.timeit('boyer_moore_search(text1, pattern)', globals=globals(),number=iter_no)
t1_3 = timeit.timeit('rabin_karp_search(text1, pattern)', globals=globals(),number=iter_no)

t1_dict = { t1_1:search1, t1_2: search2, t1_3: search3}
t1 = list(t1_dict.keys())
t1 = sorted(t1)
t1_fastest = t1_dict[t1[0]]

print("-" * 100)
print("Test 1: 'стаття 1.txt' - MATCH EXISTS - text length: ", len(text1))
print(f'  Алгоритм Кнута-Морріса-Пратта  - пошук iснуючoї фрази у "стаття 1.txt" {iter_no} iтерацiй (ceк): ', t1_1)
print(f'            Алгоритм Боєра-Мура  - пошук iснуючoї фрази у "стаття 1.txt" {iter_no} iтерацiй (ceк): ', t1_2)
print(f'          Алгоритм Рабіна-Карпа  - пошук iснуючoї фрази у "стаття 1.txt" {iter_no} iтерацiй (ceк): ', t1_3)
print("-" * 100)
print("Test 1 results:")
for i in range(0,3):
    print(f"  {i+1} place - {t1_dict[t1[i]]}")
print("FASTEST RESULT: ", t1_fastest)
print("-" * 100)


t2_1 = timeit.timeit('kmp_search(text1, false_pattern)', globals=globals(),number=iter_no)
t2_2 = timeit.timeit('boyer_moore_search(text1, false_pattern)', globals=globals(),number=iter_no)
t2_3 = timeit.timeit('rabin_karp_search(text1, false_pattern)', globals=globals(),number=iter_no)

t2_dict = { t2_1:search1, t2_2: search2, t2_3: search3}
t2 = list(t2_dict.keys())
t2 = sorted(t2)
t2_fastest = t2_dict[t2[0]]

print("-" * 100)
print("Test 2: 'стаття 1.txt' - NO MATCH - text length: ", len(text1))
print(f'  Алгоритм Кнута-Морріса-Пратта  - пошук неiснуючoї фрази у "стаття 1.txt" {iter_no} iтерацiй (ceк): ', t2_1)
print(f'            Алгоритм Боєра-Мура  - пошук неiснуючoї фрази у "стаття 1.txt" {iter_no} iтерацiй (ceк): ', t2_2)
print(f'          Алгоритм Рабіна-Карпа  - пошук неiснуючoї фрази у "стаття 1.txt" {iter_no} iтерацiй (ceк): ', t2_3)
print("-" * 100)
print("Test 2 results:")
for i in range(0,3):
    print(f"  {i+1} place - {t2_dict[t2[i]]}")
print("FASTEST RESULT: ", t2_fastest)
print("-" * 100)


t3_1 = timeit.timeit('kmp_search(text2, pattern)', globals=globals(),number=iter_no)
t3_2 = timeit.timeit('boyer_moore_search(text2, pattern)', globals=globals(),number=iter_no)
t3_3 = timeit.timeit('rabin_karp_search(text2, pattern)', globals=globals(),number=iter_no)

t3_dict = { t3_1:search1, t3_2: search2, t3_3: search3}
t3 = list(t3_dict.keys())
t3 = sorted(t3)
t3_fastest = t3_dict[t3[0]]

print("-" * 100)
print("Test 3: 'стаття 2.txt' - MATCH EXISTS - text length: ", len(text2))
print(f'  Алгоритм Кнута-Морріса-Пратта  - пошук iснуючoї фрази у "стаття 2.txt" {iter_no} iтерацiй (ceк): ', t3_1)
print(f'            Алгоритм Боєра-Мура  - пошук iснуючoї фрази у "стаття 2.txt" {iter_no} iтерацiй (ceк): ', t3_2)
print(f'          Алгоритм Рабіна-Карпа  - пошук iснуючoї фрази у "стаття 2.txt" {iter_no} iтерацiй (ceк): ', t3_3)
print("-" * 100)
print("Test 3 results:")
for i in range(0,3):
    print(f"  {i+1} place - {t3_dict[t3[i]]}")
print("FASTEST RESULT: ", t3_fastest)
print("-" * 100)


t4_1 = timeit.timeit('kmp_search(text2, false_pattern)', globals=globals(),number=iter_no)
t4_2 = timeit.timeit('boyer_moore_search(text2, false_pattern)', globals=globals(),number=iter_no)
t4_3 = timeit.timeit('rabin_karp_search(text2, false_pattern)', globals=globals(),number=iter_no)

t4_dict = { t4_1:search1, t4_2: search2, t4_3: search3}
t4 = list(t4_dict.keys())
t4 = sorted(t4)
t4_fastest = t4_dict[t4[0]]

print("-" * 100)
print("Test 4: 'стаття 2.txt' - NO MATCH - text length: ", len(text2))
print(f'  Алгоритм Кнута-Морріса-Пратта  - пошук неiснуючoї фрази у "стаття 2.txt" {iter_no} iтерацiй (ceк): ', t4_1)
print(f'            Алгоритм Боєра-Мура  - пошук неiснуючoї фрази у "стаття 2.txt" {iter_no} iтерацiй (ceк): ', t4_2)
print(f'          Алгоритм Рабіна-Карпа  - пошук неiснуючoї фрази у "стаття 2.txt" {iter_no} iтерацiй (ceк): ', t4_3)
print("-" * 100)
print("Test 4 results:")
for i in range(0,3):
    print(f"  {i+1} place - {t4_dict[t4[i]]}")
print("FASTEST RESULT: ", t4_fastest)
print("-" * 100)
