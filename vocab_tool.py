import csv
from weekpath import CSV_PATH, OUTPUT_PATH


def load_words():
    """读取生词表csv，自动尝试utf-8和gbk两种编码"""
    words = []
    # 先试utf-8，失败就试gbk（Windows Excel保存的csv经常是gbk）
    for encoding in ["utf-8", "gbk"]:
        try:
            with open(CSV_PATH, "r", encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 跳过空行
                    if row.get("词汇"):
                        words.append(row)
            if words:
                print(f"✅ 读取成功（编码：{encoding}）")
                break
        except UnicodeDecodeError:
            continue
    if not words:
        print("❌ 没读到任何数据，请检查data文件夹里有没有生词表.csv")
    return words


def filter_by_level(word_list, target_level):
    """筛选指定HSK等级的词汇"""
    result = []
    for w in word_list:
        if w.get("HSK等级", "").strip() == str(target_level):
            result.append(w)
    return result


def count_by_pos(word_list):
    """统计词性分布并打印"""
    pos_count = {}
    for w in word_list:
        pos = w.get("词性", "未知").strip()
        pos_count[pos] = pos_count.get(pos, 0) + 1
    print(f"筛选后词汇数量：{len(word_list)}")
    print("词性统计：")
    for k, v in pos_count.items():
        print(f"  {k}: {v}个")
    return pos_count


def gen_exercises(word_list):
    """生成练习.txt，每行：用"XX"造一个句子。（词性）"""
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for w in word_list:
            word = w.get("词汇", "").strip()
            pos = w.get("词性", "").strip()
            line = f'用"{word}"造一个句子。（{pos}）\n'
            f.write(line)
    print(f"✅ 练习.txt 已生成，共 {len(word_list)} 道题")


if __name__ == "__main__":
    print("=" * 30)
    all_words = load_words()
    print(f"csv总词汇数：{len(all_words)}")

    # 筛选HSK4
    hsk4_words = filter_by_level(all_words, 4)
    count_by_pos(hsk4_words)

    # 生成练习
    gen_exercises(hsk4_words)
    print("=" * 30)
