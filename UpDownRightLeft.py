if pygame.K_UP in keys:
    pointup()
    moving(True)
    if pygame.K_m in keys:
        summonFireball(100,0)
if pygame.K_RIGHT in keys:
    pointright()
    moving(True)
    if pygame.K_m in keys:
        summonFireball(100,1)
if pygame.K_LEFT in keys:
    pointleft()
    moving(True)
    if pygame.K_m in keys:
        summonFireball(100,2)
if pygame.K_DOWN in keys:
    pointdown()
    moving(True)
    if pygame.K_m in keys:
        summonFireball(100,3)
if pygame.K_RSHIFT in keys:
    swingsword()
    if pygame.K_m in keys:
        summonFireball(100,4)
if pygame.K_n in keys:
    summonFireball(1,0)
if pygame.K_o in newkeys:
    for i in range(360):
        summonFireball(0,i/1000.0)
