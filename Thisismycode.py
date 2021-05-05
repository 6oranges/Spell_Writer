if pygame.K_UP in keys:
    pointup()
    moving(True)
if pygame.K_RIGHT in keys:
    pointright()
    moving(True)
if pygame.K_LEFT in keys:
    pointleft()
    moving(True)
if pygame.K_DOWN in keys:
    pointdown()
    moving(True)
if pygame.K_SPACE in keys:
    swingsword()
if pygame.K_m in keys:
    summonFireball(100,0)
if pygame.K_n in keys:
    summonFireball(1,0)
