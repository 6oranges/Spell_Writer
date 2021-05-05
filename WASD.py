if pygame.K_w in keys:
    pointup()
    moving(True)
    if pygame.K_m in keys:
        summonFireball(100,0)
if pygame.K_d in keys:
    pointright()
    moving(True)
    if pygame.K_m in keys:
        summonFireball(100,1)
if pygame.K_a in keys:
    pointleft()
    moving(True)
    if pygame.K_m in keys:
        summonFireball(100,2)
if pygame.K_s in keys:
    pointdown()
    moving(True)
    if pygame.K_m in keys:
        summonFireball(100,3)
if pygame.K_q in keys:
    swingsword()
    if pygame.K_m in keys:
        summonFireball(100,4)

