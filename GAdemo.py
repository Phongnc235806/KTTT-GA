import random
import string

# --- CẤU HÌNH BÀI TOÁN ---
TARGET_PHRASE = "Genetic Algorithm Project 143"  # Chuỗi mục tiêu cần tìm
POPULATION_SIZE = 100         # Kích thước quần thể 
MUTATION_RATE = 0.01          # Tỷ lệ đột biến [cite: 16]

# --- CÁC HÀM CỐT LÕI CỦA GA ---

def create_genome(length):
    """Khởi tạo gen ngẫu nhiên cho một cá thể"""
    characters = string.ascii_letters + string.digits + " " + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def create_population(pop_size, target_length):
    """B1: Khởi tạo quần thể ban đầu [cite: 19]"""
    return [create_genome(target_length) for _ in range(pop_size)]

def fitness(genome, target):
    """Hàm đánh giá (Fitness Function) 
    Đếm số ký tự trùng khớp với chuỗi mục tiêu."""
    score = 0
    for i in range(len(genome)):
        if genome[i] == target[i]:
            score += 1
    return score

def selection(population, target):
    """B3: Tạo bể lai ghép & Chọn lọc (Selection) [cite: 12, 21]
    Chọn các cá thể tốt nhất để làm cha mẹ (Tournament Selection đơn giản)."""
    # Sắp xếp quần thể theo điểm fitness giảm dần
    sorted_pop = sorted(population, key=lambda x: fitness(x, target), reverse=True)
    # Lấy 50% cá thể tốt nhất (Elitism GA - giữ lại nghiệm tốt) [cite: 34]
    return sorted_pop[:int(POPULATION_SIZE * 0.5)]

def crossover(parent1, parent2):
    """Lai ghép (Crossover) [cite: 14]
    Lấy một nửa gen từ cha và một nửa từ mẹ."""
    split_idx = random.randint(1, len(parent1) - 1)
    child = parent1[:split_idx] + parent2[split_idx:]
    return child

def mutate(genome):
    """Đột biến (Mutation) [cite: 16]
    Thay đổi ngẫu nhiên ký tự với xác suất thấp để duy trì sự đa dạng."""
    genome_list = list(genome)
    for i in range(len(genome_list)):
        if random.random() < MUTATION_RATE:
            characters = string.ascii_letters + string.digits + " " + string.punctuation
            genome_list[i] = random.choice(characters)
    return ''.join(genome_list)

# --- CHƯƠNG TRÌNH CHÍNH (MAIN LOOP) ---

def main():
    # B1: Khởi tạo quần thể
    population = create_population(POPULATION_SIZE, len(TARGET_PHRASE))
    generation = 1
    
    while True:
        # B2 & B6: Tính giá trị thích nghi
        # Tìm cá thể tốt nhất trong thế hệ hiện tại
        best_individual = max(population, key=lambda x: fitness(x, TARGET_PHRASE))
        current_fitness = fitness(best_individual, TARGET_PHRASE)
        
        print(f"Thế hệ {generation} | Best: {best_individual} | Fitness: {current_fitness}/{len(TARGET_PHRASE)}")
        
        # B8: Kiểm tra điều kiện dừng (Nếu tìm thấy chuỗi mục tiêu) [cite: 17, 26]
        if current_fitness == len(TARGET_PHRASE):
            print("\n>>> Đã tìm thấy giải pháp tối ưu!")
            break

        # B3: Chọn lọc cha mẹ
        parents = selection(population, TARGET_PHRASE)
        
        # B4: Tạo thế hệ mới
        new_population = []
        
        # Giữ lại top parents cho thế hệ sau (đảm bảo không bị mất gen tốt)
        new_population.extend(parents) 
        
        # Sinh sản để lấp đầy quần thể
        while len(new_population) < POPULATION_SIZE:
            p1 = random.choice(parents)
            p2 = random.choice(parents)
            
            # B5: Lai ghép và Đột biến [cite: 23]
            child = crossover(p1, p2)
            child = mutate(child)
            new_population.append(child)
            
        # B7: Cập nhật quần thể
        population = new_population
        generation += 1

if __name__ == "__main__":
    main()