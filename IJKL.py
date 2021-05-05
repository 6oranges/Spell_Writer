if pygame.K_i in keys:
    pointup()
    moving(True)
elif pygame.K_l in keys:
    pointright()
    moving(True)
elif pygame.K_j in keys:
    pointleft()
    moving(True)
elif pygame.K_k in keys:
    pointdown()
    moving(True)
else:
    moving(False)
if pygame.K_SPACE in keys:
    swingsword()

