#Task1
# Utility function to calculate the score of a gene sequence
def CalculateUtility(Gene, Target, Weights):
    Score = 0
    MaxLen = max(len(Gene), len(Target))
    
    for I in range(MaxLen):
        GeneChar = ord(Gene[I]) if I < len(Gene) else 0
        TargetChar = ord(Target[I]) if I < len(Target) else 0
        Weight = Weights[I] if I < len(Weights) else 1
        Score += Weight * abs(GeneChar - TargetChar)
    
    return -Score  # Lower penalty is better

# Minimax with alpha-beta pruning (now using PascalCase variable names)
def Minimax(Pool, Gene, Target, Weights, IsMaxTurn, AbMin, AbMax):
    if not Pool:
        return CalculateUtility(Gene, Target, Weights), Gene

    if IsMaxTurn:
        MaxScore = float('-inf')
        BestSeq = ""
        for I in range(len(Pool)):
            NewGene = Gene + Pool[I]
            NewPool = Pool[:I] + Pool[I+1:]
            Score, Seq = Minimax(NewPool, NewGene, Target, Weights, False, AbMin, AbMax)
            if Score > MaxScore:
                MaxScore = Score
                BestSeq = Seq
            AbMin = max(AbMin, Score)
            if AbMax <= AbMin:
                break
        return MaxScore, BestSeq
    else:
        MinScore = float('inf')
        BestSeq = ""
        for I in range(len(Pool)):
            NewGene = Gene + Pool[I]
            NewPool = Pool[:I] + Pool[I+1:]
            Score, Seq = Minimax(NewPool, NewGene, Target, Weights, True, AbMin, AbMax)
            if Score < MinScore:
                MinScore = Score
                BestSeq = Seq
            AbMax = min(AbMax, Score)
            if AbMax <= AbMin:
                break
        return MinScore, BestSeq

# Main program
def Main():
    with open('input.txt', 'r') as File:
        PoolLine = File.readline().strip()
        Target = File.readline().strip()
        StudentIdLine = File.readline().strip()

    Pool = PoolLine.split(',')
    StudentIdDigits = list(map(int, StudentIdLine.split()))
    Weights = StudentIdDigits[-len(Target):]  # Extract weights

    Score, BestGene = Minimax(Pool, "", Target, Weights, True, float('-inf'), float('inf'))

    with open('output.txt', 'w') as File:
        File.write(BestGene + '\n')
        File.write(str(Score) + '\n')

if __name__ == "__main__":
    Main()





#Task2
# def CalculateUtility(Gene, Target, Weights):
#     Score = 0
#     MaxLen = max(len(Gene), len(Target))
    
#     for I in range(MaxLen):
#         GeneChar = ord(Gene[I]) if I < len(Gene) else 0
#         TargetChar = ord(Target[I]) if I < len(Target) else 0
#         Weight = Weights[I] if I < len(Weights) else 1
#         Score += Weight * abs(GeneChar - TargetChar)
    
#     return -Score

# def ApplyBooster(Weights, Position, Booster):
#     NewWeights = []
#     for I in range(len(Weights)):
#         if I >= Position:
#             NewWeights.append(Weights[I] * Booster)
#         else:
#             NewWeights.append(Weights[I])
#     return NewWeights

# def Minimax(Pool, Gene, Target, Weights, IsMaxTurn, AbMin, AbMax, Booster=None, UsedBooster=False):
#     if not Pool:
#         return CalculateUtility(Gene, Target, Weights), Gene

#     if IsMaxTurn:
#         MaxScore = float('-inf')
#         BestSeq = ""
#         for I in range(len(Pool)):
#             Nuc = Pool[I]
#             NewGene = Gene + Nuc
#             NewPool = Pool[:I] + Pool[I+1:]

#             NewWeights = Weights
#             BoosterUsed = UsedBooster

#             # Apply booster if 'S' is picked by Agent 1 and not already boosted
#             if Nuc == 'S' and Booster is not None and not UsedBooster:
#                 NewWeights = ApplyBooster(Weights, len(Gene), Booster)
#                 BoosterUsed = True

#             Score, Seq = Minimax(NewPool, NewGene, Target, NewWeights, False, AbMin, AbMax, Booster, BoosterUsed)
#             if Score > MaxScore:
#                 MaxScore = Score
#                 BestSeq = Seq
#             AbMin = max(AbMin, Score)
#             if AbMax <= AbMin:
#                 break
#         return MaxScore, BestSeq
#     else:
#         MinScore = float('inf')
#         BestSeq = ""
#         for I in range(len(Pool)):
#             Nuc = Pool[I]
#             NewGene = Gene + Nuc
#             NewPool = Pool[:I] + Pool[I+1:]

#             Score, Seq = Minimax(NewPool, NewGene, Target, Weights, True, AbMin, AbMax, Booster, UsedBooster)
#             if Score < MinScore:
#                 MinScore = Score
#                 BestSeq = Seq
#             AbMax = min(AbMax, Score)
#             if AbMax <= AbMin:
#                 break
#         return MinScore, BestSeq

# def Main():
#     with open('input2.txt', 'r') as File:
#         PoolLine = File.readline().strip()
#         Target = File.readline().strip()
#         StudentIdLine = File.readline().strip()

#     Pool = PoolLine.split(',')
#     Target = Target.strip()
#     StudentIdDigits = list(map(int, StudentIdLine.split()))

#     FirstTwoDigits = int(str(StudentIdDigits[0]) + str(StudentIdDigits[1]))
#     Booster = FirstTwoDigits / 100
#     Weights = StudentIdDigits[-len(Target):]

#     # Scenario 1: Without S
#     Score1, i = Minimax(Pool, "", Target, Weights, True, float('-inf'), float('inf'))

#     # Scenario 2: With S in the pool
#     PoolWithS = Pool + ['S']
#     Score2, BestGene2 = Minimax(PoolWithS, "", Target, Weights, True, float('-inf'), float('inf'), Booster, False)

#     # Compare
#     Decision = "YES" if Score2 > Score1 else "NO"

#     with open('output2.txt', 'w') as File:
#         File.write(Decision + '\n')
#         File.write("Best gene sequence generated: " + BestGene2 + '\n')
#         File.write("Utility score: " + str(Score2) + '\n')

# if __name__ == "__main__":
#     Main()

