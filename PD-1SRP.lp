\ Model Location-based model-total capacity
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  53 vars[0,1] + 79 vars[0,2] + 50 vars[0,3] + 96 vars[0,4] + 19 vars[0,5]
   + 59 vars[0,6] + 24 vars[0,7] + 49 vars[0,8] + 83 vars[0,9]
   + 43 vars[0,10] + 0 vars[1,0] + 69 vars[1,2] + 29 vars[1,3]
   + 62 vars[1,4] + 59 vars[1,5] + 69 vars[1,6] + 38 vars[1,7]
   + 32 vars[1,8] + 32 vars[1,9] + 31 vars[1,10] + 53 vars[1,11]
   + 0 vars[2,0] + 69 vars[2,1] + 41 vars[2,3] + 38 vars[2,4]
   + 96 vars[2,5] + 29 vars[2,6] + 57 vars[2,7] + 96 vars[2,8]
   + 88 vars[2,9] + 92 vars[2,10] + 79 vars[2,11] + 0 vars[3,0]
   + 29 vars[3,1] + 41 vars[3,2] + 47 vars[3,4] + 64 vars[3,5]
   + 42 vars[3,6] + 27 vars[3,7] + 56 vars[3,8] + 55 vars[3,9]
   + 52 vars[3,10] + 50 vars[3,11] + 0 vars[4,0] + 62 vars[4,1]
   + 38 vars[4,2] + 47 vars[4,3] + 110 vars[4,5] + 62 vars[4,6]
   + 72 vars[4,7] + 94 vars[4,8] + 68 vars[4,9] + 92 vars[4,10]
   + 96 vars[4,11] + 0 vars[5,0] + 59 vars[5,1] + 96 vars[5,2]
   + 64 vars[5,3] + 110 vars[5,4] + 78 vars[5,6] + 40 vars[5,7]
   + 44 vars[5,8] + 86 vars[5,9] + 40 vars[5,10] + 19 vars[5,11]
   + 0 vars[6,0] + 69 vars[6,1] + 29 vars[6,2] + 42 vars[6,3]
   + 62 vars[6,4] + 78 vars[6,5] + 43 vars[6,7] + 90 vars[6,8]
   + 96 vars[6,9] + 85 vars[6,10] + 59 vars[6,11] + 0 vars[7,0]
   + 38 vars[7,1] + 57 vars[7,2] + 27 vars[7,3] + 72 vars[7,4]
   + 40 vars[7,5] + 43 vars[7,6] + 49 vars[7,8] + 69 vars[7,9]
   + 43 vars[7,10] + 24 vars[7,11] + 0 vars[8,0] + 32 vars[8,1]
   + 96 vars[8,2] + 56 vars[8,3] + 94 vars[8,4] + 44 vars[8,5]
   + 90 vars[8,6] + 49 vars[8,7] + 47 vars[8,9] + 6 vars[8,10]
   + 49 vars[8,11] + 0 vars[9,0] + 32 vars[9,1] + 88 vars[9,2]
   + 55 vars[9,3] + 68 vars[9,4] + 86 vars[9,5] + 96 vars[9,6]
   + 69 vars[9,7] + 47 vars[9,8] + 49 vars[9,10] + 83 vars[9,11]
   + 0 vars[10,0] + 31 vars[10,1] + 92 vars[10,2] + 52 vars[10,3]
   + 92 vars[10,4] + 40 vars[10,5] + 85 vars[10,6] + 43 vars[10,7]
   + 6 vars[10,8] + 49 vars[10,9] + 43 vars[10,11] + 0 vars[11,0]
   + 0 vars[11,1] + 0 vars[11,2] + 0 vars[11,3] + 0 vars[11,4]
   + 0 vars[11,5] + 0 vars[11,6] + 0 vars[11,7] + 0 vars[11,8]
   + 0 vars[11,9] + 0 vars[11,10]
Subject To
 R0: t[0] = 0
 R1: c[0] = 700
 R2: sigma[0] = 1
 leaving0: vars[0,1] + vars[0,2] + vars[0,3] + vars[0,4] + vars[0,5]
   + vars[0,6] + vars[0,7] + vars[0,8] + vars[0,9] + vars[0,10]
   + vars[0,11] = 1
 leaving1: vars[1,2] + vars[1,3] + vars[1,4] + vars[1,5] + vars[1,6]
   + vars[1,7] + vars[1,8] + vars[1,9] + vars[1,10] + vars[1,11] = 1
 leaving2: vars[2,1] + vars[2,3] + vars[2,4] + vars[2,5] + vars[2,6]
   + vars[2,7] + vars[2,8] + vars[2,9] + vars[2,10] + vars[2,11] = 1
 leaving3: vars[3,1] + vars[3,2] + vars[3,4] + vars[3,5] + vars[3,6]
   + vars[3,7] + vars[3,8] + vars[3,9] + vars[3,10] + vars[3,11] = 1
 leaving4: vars[4,1] + vars[4,2] + vars[4,3] + vars[4,5] + vars[4,6]
   + vars[4,7] + vars[4,8] + vars[4,9] + vars[4,10] + vars[4,11] = 1
 leaving5: vars[5,1] + vars[5,2] + vars[5,3] + vars[5,4] + vars[5,6]
   + vars[5,7] + vars[5,8] + vars[5,9] + vars[5,10] + vars[5,11] = 1
 leaving6: vars[6,1] + vars[6,2] + vars[6,3] + vars[6,4] + vars[6,5]
   + vars[6,7] + vars[6,8] + vars[6,9] + vars[6,10] + vars[6,11] = 1
 leaving7: vars[7,1] + vars[7,2] + vars[7,3] + vars[7,4] + vars[7,5]
   + vars[7,6] + vars[7,8] + vars[7,9] + vars[7,10] + vars[7,11] = 1
 leaving8: vars[8,1] + vars[8,2] + vars[8,3] + vars[8,4] + vars[8,5]
   + vars[8,6] + vars[8,7] + vars[8,9] + vars[8,10] + vars[8,11] = 1
 leaving9: vars[9,1] + vars[9,2] + vars[9,3] + vars[9,4] + vars[9,5]
   + vars[9,6] + vars[9,7] + vars[9,8] + vars[9,10] + vars[9,11] = 1
 leaving10: vars[10,1] + vars[10,2] + vars[10,3] + vars[10,4] + vars[10,5]
   + vars[10,6] + vars[10,7] + vars[10,8] + vars[10,9] + vars[10,11] = 1
 balanced1: - vars[0,1] + vars[1,2] + vars[1,3] + vars[1,4] + vars[1,5]
   + vars[1,6] + vars[1,7] + vars[1,8] + vars[1,9] + vars[1,10]
   + vars[1,11] - vars[2,1] - vars[3,1] - vars[4,1] - vars[5,1] - vars[6,1]
   - vars[7,1] - vars[8,1] - vars[9,1] - vars[10,1] = 0
 balanced2: - vars[0,2] - vars[1,2] + vars[2,1] + vars[2,3] + vars[2,4]
   + vars[2,5] + vars[2,6] + vars[2,7] + vars[2,8] + vars[2,9] + vars[2,10]
   + vars[2,11] - vars[3,2] - vars[4,2] - vars[5,2] - vars[6,2] - vars[7,2]
   - vars[8,2] - vars[9,2] - vars[10,2] = 0
 balanced3: - vars[0,3] - vars[1,3] - vars[2,3] + vars[3,1] + vars[3,2]
   + vars[3,4] + vars[3,5] + vars[3,6] + vars[3,7] + vars[3,8] + vars[3,9]
   + vars[3,10] + vars[3,11] - vars[4,3] - vars[5,3] - vars[6,3]
   - vars[7,3] - vars[8,3] - vars[9,3] - vars[10,3] = 0
 balanced4: - vars[0,4] - vars[1,4] - vars[2,4] - vars[3,4] + vars[4,1]
   + vars[4,2] + vars[4,3] + vars[4,5] + vars[4,6] + vars[4,7] + vars[4,8]
   + vars[4,9] + vars[4,10] + vars[4,11] - vars[5,4] - vars[6,4]
   - vars[7,4] - vars[8,4] - vars[9,4] - vars[10,4] = 0
 balanced5: - vars[0,5] - vars[1,5] - vars[2,5] - vars[3,5] - vars[4,5]
   + vars[5,1] + vars[5,2] + vars[5,3] + vars[5,4] + vars[5,6] + vars[5,7]
   + vars[5,8] + vars[5,9] + vars[5,10] + vars[5,11] - vars[6,5]
   - vars[7,5] - vars[8,5] - vars[9,5] - vars[10,5] = 0
 balanced6: - vars[0,6] - vars[1,6] - vars[2,6] - vars[3,6] - vars[4,6]
   - vars[5,6] + vars[6,1] + vars[6,2] + vars[6,3] + vars[6,4] + vars[6,5]
   + vars[6,7] + vars[6,8] + vars[6,9] + vars[6,10] + vars[6,11]
   - vars[7,6] - vars[8,6] - vars[9,6] - vars[10,6] = 0
 balanced7: - vars[0,7] - vars[1,7] - vars[2,7] - vars[3,7] - vars[4,7]
   - vars[5,7] - vars[6,7] + vars[7,1] + vars[7,2] + vars[7,3] + vars[7,4]
   + vars[7,5] + vars[7,6] + vars[7,8] + vars[7,9] + vars[7,10]
   + vars[7,11] - vars[8,7] - vars[9,7] - vars[10,7] = 0
 balanced8: - vars[0,8] - vars[1,8] - vars[2,8] - vars[3,8] - vars[4,8]
   - vars[5,8] - vars[6,8] - vars[7,8] + vars[8,1] + vars[8,2] + vars[8,3]
   + vars[8,4] + vars[8,5] + vars[8,6] + vars[8,7] + vars[8,9] + vars[8,10]
   + vars[8,11] - vars[9,8] - vars[10,8] = 0
 balanced9: - vars[0,9] - vars[1,9] - vars[2,9] - vars[3,9] - vars[4,9]
   - vars[5,9] - vars[6,9] - vars[7,9] - vars[8,9] + vars[9,1] + vars[9,2]
   + vars[9,3] + vars[9,4] + vars[9,5] + vars[9,6] + vars[9,7] + vars[9,8]
   + vars[9,10] + vars[9,11] - vars[10,9] = 0
 balanced10: - vars[0,10] - vars[1,10] - vars[2,10] - vars[3,10]
   - vars[4,10] - vars[5,10] - vars[6,10] - vars[7,10] - vars[8,10]
   - vars[9,10] + vars[10,1] + vars[10,2] + vars[10,3] + vars[10,4]
   + vars[10,5] + vars[10,6] + vars[10,7] + vars[10,8] + vars[10,9]
   + vars[10,11] = 0
 subtour_elimination0,1: 11 vars[0,1] + t[0] - t[1] <= 10
 subtour_elimination0,2: 11 vars[0,2] + t[0] - t[2] <= 10
 subtour_elimination0,3: 11 vars[0,3] + t[0] - t[3] <= 10
 subtour_elimination0,4: 11 vars[0,4] + t[0] - t[4] <= 10
 subtour_elimination0,5: 11 vars[0,5] + t[0] - t[5] <= 10
 subtour_elimination0,6: 11 vars[0,6] + t[0] - t[6] <= 10
 subtour_elimination0,7: 11 vars[0,7] + t[0] - t[7] <= 10
 subtour_elimination0,8: 11 vars[0,8] + t[0] - t[8] <= 10
 subtour_elimination0,9: 11 vars[0,9] + t[0] - t[9] <= 10
 subtour_elimination0,10: 11 vars[0,10] + t[0] - t[10] <= 10
 subtour_elimination0,11: 11 vars[0,11] + t[0] - t[11] <= 10
 subtour_elimination1,2: 11 vars[1,2] + t[1] - t[2] <= 10
 subtour_elimination1,3: 11 vars[1,3] + t[1] - t[3] <= 10
 subtour_elimination1,4: 11 vars[1,4] + t[1] - t[4] <= 10
 subtour_elimination1,5: 11 vars[1,5] + t[1] - t[5] <= 10
 subtour_elimination1,6: 11 vars[1,6] + t[1] - t[6] <= 10
 subtour_elimination1,7: 11 vars[1,7] + t[1] - t[7] <= 10
 subtour_elimination1,8: 11 vars[1,8] + t[1] - t[8] <= 10
 subtour_elimination1,9: 11 vars[1,9] + t[1] - t[9] <= 10
 subtour_elimination1,10: 11 vars[1,10] + t[1] - t[10] <= 10
 subtour_elimination1,11: 11 vars[1,11] + t[1] - t[11] <= 10
 subtour_elimination2,1: 11 vars[2,1] - t[1] + t[2] <= 10
 subtour_elimination2,3: 11 vars[2,3] + t[2] - t[3] <= 10
 subtour_elimination2,4: 11 vars[2,4] + t[2] - t[4] <= 10
 subtour_elimination2,5: 11 vars[2,5] + t[2] - t[5] <= 10
 subtour_elimination2,6: 11 vars[2,6] + t[2] - t[6] <= 10
 subtour_elimination2,7: 11 vars[2,7] + t[2] - t[7] <= 10
 subtour_elimination2,8: 11 vars[2,8] + t[2] - t[8] <= 10
 subtour_elimination2,9: 11 vars[2,9] + t[2] - t[9] <= 10
 subtour_elimination2,10: 11 vars[2,10] + t[2] - t[10] <= 10
 subtour_elimination2,11: 11 vars[2,11] + t[2] - t[11] <= 10
 subtour_elimination3,1: 11 vars[3,1] - t[1] + t[3] <= 10
 subtour_elimination3,2: 11 vars[3,2] - t[2] + t[3] <= 10
 subtour_elimination3,4: 11 vars[3,4] + t[3] - t[4] <= 10
 subtour_elimination3,5: 11 vars[3,5] + t[3] - t[5] <= 10
 subtour_elimination3,6: 11 vars[3,6] + t[3] - t[6] <= 10
 subtour_elimination3,7: 11 vars[3,7] + t[3] - t[7] <= 10
 subtour_elimination3,8: 11 vars[3,8] + t[3] - t[8] <= 10
 subtour_elimination3,9: 11 vars[3,9] + t[3] - t[9] <= 10
 subtour_elimination3,10: 11 vars[3,10] + t[3] - t[10] <= 10
 subtour_elimination3,11: 11 vars[3,11] + t[3] - t[11] <= 10
 subtour_elimination4,1: 11 vars[4,1] - t[1] + t[4] <= 10
 subtour_elimination4,2: 11 vars[4,2] - t[2] + t[4] <= 10
 subtour_elimination4,3: 11 vars[4,3] - t[3] + t[4] <= 10
 subtour_elimination4,5: 11 vars[4,5] + t[4] - t[5] <= 10
 subtour_elimination4,6: 11 vars[4,6] + t[4] - t[6] <= 10
 subtour_elimination4,7: 11 vars[4,7] + t[4] - t[7] <= 10
 subtour_elimination4,8: 11 vars[4,8] + t[4] - t[8] <= 10
 subtour_elimination4,9: 11 vars[4,9] + t[4] - t[9] <= 10
 subtour_elimination4,10: 11 vars[4,10] + t[4] - t[10] <= 10
 subtour_elimination4,11: 11 vars[4,11] + t[4] - t[11] <= 10
 subtour_elimination5,1: 11 vars[5,1] - t[1] + t[5] <= 10
 subtour_elimination5,2: 11 vars[5,2] - t[2] + t[5] <= 10
 subtour_elimination5,3: 11 vars[5,3] - t[3] + t[5] <= 10
 subtour_elimination5,4: 11 vars[5,4] - t[4] + t[5] <= 10
 subtour_elimination5,6: 11 vars[5,6] + t[5] - t[6] <= 10
 subtour_elimination5,7: 11 vars[5,7] + t[5] - t[7] <= 10
 subtour_elimination5,8: 11 vars[5,8] + t[5] - t[8] <= 10
 subtour_elimination5,9: 11 vars[5,9] + t[5] - t[9] <= 10
 subtour_elimination5,10: 11 vars[5,10] + t[5] - t[10] <= 10
 subtour_elimination5,11: 11 vars[5,11] + t[5] - t[11] <= 10
 subtour_elimination6,1: 11 vars[6,1] - t[1] + t[6] <= 10
 subtour_elimination6,2: 11 vars[6,2] - t[2] + t[6] <= 10
 subtour_elimination6,3: 11 vars[6,3] - t[3] + t[6] <= 10
 subtour_elimination6,4: 11 vars[6,4] - t[4] + t[6] <= 10
 subtour_elimination6,5: 11 vars[6,5] - t[5] + t[6] <= 10
 subtour_elimination6,7: 11 vars[6,7] + t[6] - t[7] <= 10
 subtour_elimination6,8: 11 vars[6,8] + t[6] - t[8] <= 10
 subtour_elimination6,9: 11 vars[6,9] + t[6] - t[9] <= 10
 subtour_elimination6,10: 11 vars[6,10] + t[6] - t[10] <= 10
 subtour_elimination6,11: 11 vars[6,11] + t[6] - t[11] <= 10
 subtour_elimination7,1: 11 vars[7,1] - t[1] + t[7] <= 10
 subtour_elimination7,2: 11 vars[7,2] - t[2] + t[7] <= 10
 subtour_elimination7,3: 11 vars[7,3] - t[3] + t[7] <= 10
 subtour_elimination7,4: 11 vars[7,4] - t[4] + t[7] <= 10
 subtour_elimination7,5: 11 vars[7,5] - t[5] + t[7] <= 10
 subtour_elimination7,6: 11 vars[7,6] - t[6] + t[7] <= 10
 subtour_elimination7,8: 11 vars[7,8] + t[7] - t[8] <= 10
 subtour_elimination7,9: 11 vars[7,9] + t[7] - t[9] <= 10
 subtour_elimination7,10: 11 vars[7,10] + t[7] - t[10] <= 10
 subtour_elimination7,11: 11 vars[7,11] + t[7] - t[11] <= 10
 subtour_elimination8,1: 11 vars[8,1] - t[1] + t[8] <= 10
 subtour_elimination8,2: 11 vars[8,2] - t[2] + t[8] <= 10
 subtour_elimination8,3: 11 vars[8,3] - t[3] + t[8] <= 10
 subtour_elimination8,4: 11 vars[8,4] - t[4] + t[8] <= 10
 subtour_elimination8,5: 11 vars[8,5] - t[5] + t[8] <= 10
 subtour_elimination8,6: 11 vars[8,6] - t[6] + t[8] <= 10
 subtour_elimination8,7: 11 vars[8,7] - t[7] + t[8] <= 10
 subtour_elimination8,9: 11 vars[8,9] + t[8] - t[9] <= 10
 subtour_elimination8,10: 11 vars[8,10] + t[8] - t[10] <= 10
 subtour_elimination8,11: 11 vars[8,11] + t[8] - t[11] <= 10
 subtour_elimination9,1: 11 vars[9,1] - t[1] + t[9] <= 10
 subtour_elimination9,2: 11 vars[9,2] - t[2] + t[9] <= 10
 subtour_elimination9,3: 11 vars[9,3] - t[3] + t[9] <= 10
 subtour_elimination9,4: 11 vars[9,4] - t[4] + t[9] <= 10
 subtour_elimination9,5: 11 vars[9,5] - t[5] + t[9] <= 10
 subtour_elimination9,6: 11 vars[9,6] - t[6] + t[9] <= 10
 subtour_elimination9,7: 11 vars[9,7] - t[7] + t[9] <= 10
 subtour_elimination9,8: 11 vars[9,8] - t[8] + t[9] <= 10
 subtour_elimination9,10: 11 vars[9,10] + t[9] - t[10] <= 10
 subtour_elimination9,11: 11 vars[9,11] + t[9] - t[11] <= 10
 subtour_elimination10,1: 11 vars[10,1] - t[1] + t[10] <= 10
 subtour_elimination10,2: 11 vars[10,2] - t[2] + t[10] <= 10
 subtour_elimination10,3: 11 vars[10,3] - t[3] + t[10] <= 10
 subtour_elimination10,4: 11 vars[10,4] - t[4] + t[10] <= 10
 subtour_elimination10,5: 11 vars[10,5] - t[5] + t[10] <= 10
 subtour_elimination10,6: 11 vars[10,6] - t[6] + t[10] <= 10
 subtour_elimination10,7: 11 vars[10,7] - t[7] + t[10] <= 10
 subtour_elimination10,8: 11 vars[10,8] - t[8] + t[10] <= 10
 subtour_elimination10,9: 11 vars[10,9] - t[9] + t[10] <= 10
 subtour_elimination10,11: 11 vars[10,11] + t[10] - t[11] <= 10
 precedence1: t[1] - t[6] <= -1
 precedence2: t[2] - t[7] <= -1
 precedence3: t[3] - t[8] <= -1
 precedence4: t[4] - t[9] <= -1
 precedence5: t[5] - t[10] <= -1
 subtour_elimination_domain1: t[1] >= 1
 subtour_elimination_domain2: t[2] >= 1
 subtour_elimination_domain3: t[3] >= 1
 subtour_elimination_domain4: t[4] >= 1
 subtour_elimination_domain5: t[5] >= 1
 subtour_elimination_domain6: t[6] >= 1
 subtour_elimination_domain7: t[7] >= 1
 subtour_elimination_domain8: t[8] >= 1
 subtour_elimination_domain9: t[9] >= 1
 subtour_elimination_domain10: t[10] >= 1
 subtour_elimination_domain1: t[1] <= 10
 subtour_elimination_domain2: t[2] <= 10
 subtour_elimination_domain3: t[3] <= 10
 subtour_elimination_domain4: t[4] <= 10
 subtour_elimination_domain5: t[5] <= 10
 subtour_elimination_domain6: t[6] <= 10
 subtour_elimination_domain7: t[7] <= 10
 subtour_elimination_domain8: t[8] <= 10
 subtour_elimination_domain9: t[9] <= 10
 subtour_elimination_domain10: t[10] <= 10
 total_cap1: 100 sigma[1] + c[1] = 800
 total_cap2: 100 sigma[2] + c[2] = 800
 total_cap3: 100 sigma[3] + c[3] = 800
 total_cap4: 100 sigma[4] + c[4] = 800
 total_cap5: 100 sigma[5] + c[5] = 800
 total_cap6: 100 sigma[6] + c[6] = 800
 total_cap7: 100 sigma[7] + c[7] = 800
 total_cap8: 100 sigma[8] + c[8] = 800
 total_cap9: 100 sigma[9] + c[9] = 800
 total_cap10: 100 sigma[10] + c[10] = 800
 total_cap11: 100 sigma[11] + c[11] = 800
 passenger_delivery0,1: 7 vars[0,1] - sigma[0] + sigma[1] <= 12
 passenger_delivery0,2: 6 vars[0,2] - sigma[0] + sigma[2] <= 12
 passenger_delivery0,3: 6 vars[0,3] - sigma[0] + sigma[3] <= 12
 passenger_delivery0,4: 9 vars[0,4] - sigma[0] + sigma[4] <= 12
 passenger_delivery0,5: 6 vars[0,5] - sigma[0] + sigma[5] <= 12
 passenger_delivery0,6: 6 vars[0,6] - sigma[0] + sigma[6] <= 12
 passenger_delivery0,7: 11 vars[0,7] - sigma[0] + sigma[7] <= 12
 passenger_delivery0,8: 9 vars[0,8] - sigma[0] + sigma[8] <= 12
 passenger_delivery0,9: 12 vars[0,9] - sigma[0] + sigma[9] <= 12
 passenger_delivery0,10: 10 vars[0,10] - sigma[0] + sigma[10] <= 12
 passenger_delivery1,2: 6 vars[1,2] - sigma[1] + sigma[2] <= 12
 passenger_delivery1,3: 6 vars[1,3] - sigma[1] + sigma[3] <= 12
 passenger_delivery1,4: 9 vars[1,4] - sigma[1] + sigma[4] <= 12
 passenger_delivery1,5: 6 vars[1,5] - sigma[1] + sigma[5] <= 12
 passenger_delivery1,6: 6 vars[1,6] - sigma[1] + sigma[6] <= 12
 passenger_delivery1,7: 11 vars[1,7] - sigma[1] + sigma[7] <= 12
 passenger_delivery1,8: 9 vars[1,8] - sigma[1] + sigma[8] <= 12
 passenger_delivery1,9: 12 vars[1,9] - sigma[1] + sigma[9] <= 12
 passenger_delivery1,10: 10 vars[1,10] - sigma[1] + sigma[10] <= 12
 passenger_delivery2,1: 7 vars[2,1] + sigma[1] - sigma[2] <= 12
 passenger_delivery2,3: 6 vars[2,3] - sigma[2] + sigma[3] <= 12
 passenger_delivery2,4: 9 vars[2,4] - sigma[2] + sigma[4] <= 12
 passenger_delivery2,5: 6 vars[2,5] - sigma[2] + sigma[5] <= 12
 passenger_delivery2,6: 6 vars[2,6] - sigma[2] + sigma[6] <= 12
 passenger_delivery2,7: 11 vars[2,7] - sigma[2] + sigma[7] <= 12
 passenger_delivery2,8: 9 vars[2,8] - sigma[2] + sigma[8] <= 12
 passenger_delivery2,9: 12 vars[2,9] - sigma[2] + sigma[9] <= 12
 passenger_delivery2,10: 10 vars[2,10] - sigma[2] + sigma[10] <= 12
 passenger_delivery3,1: 7 vars[3,1] + sigma[1] - sigma[3] <= 12
 passenger_delivery3,2: 6 vars[3,2] + sigma[2] - sigma[3] <= 12
 passenger_delivery3,4: 9 vars[3,4] - sigma[3] + sigma[4] <= 12
 passenger_delivery3,5: 6 vars[3,5] - sigma[3] + sigma[5] <= 12
 passenger_delivery3,6: 6 vars[3,6] - sigma[3] + sigma[6] <= 12
 passenger_delivery3,7: 11 vars[3,7] - sigma[3] + sigma[7] <= 12
 passenger_delivery3,8: 9 vars[3,8] - sigma[3] + sigma[8] <= 12
 passenger_delivery3,9: 12 vars[3,9] - sigma[3] + sigma[9] <= 12
 passenger_delivery3,10: 10 vars[3,10] - sigma[3] + sigma[10] <= 12
 passenger_delivery4,1: 7 vars[4,1] + sigma[1] - sigma[4] <= 12
 passenger_delivery4,2: 6 vars[4,2] + sigma[2] - sigma[4] <= 12
 passenger_delivery4,3: 6 vars[4,3] + sigma[3] - sigma[4] <= 12
 passenger_delivery4,5: 6 vars[4,5] - sigma[4] + sigma[5] <= 12
 passenger_delivery4,6: 6 vars[4,6] - sigma[4] + sigma[6] <= 12
 passenger_delivery4,7: 11 vars[4,7] - sigma[4] + sigma[7] <= 12
 passenger_delivery4,8: 9 vars[4,8] - sigma[4] + sigma[8] <= 12
 passenger_delivery4,9: 12 vars[4,9] - sigma[4] + sigma[9] <= 12
 passenger_delivery4,10: 10 vars[4,10] - sigma[4] + sigma[10] <= 12
 passenger_delivery5,1: 7 vars[5,1] + sigma[1] - sigma[5] <= 12
 passenger_delivery5,2: 6 vars[5,2] + sigma[2] - sigma[5] <= 12
 passenger_delivery5,3: 6 vars[5,3] + sigma[3] - sigma[5] <= 12
 passenger_delivery5,4: 9 vars[5,4] + sigma[4] - sigma[5] <= 12
 passenger_delivery5,6: 6 vars[5,6] - sigma[5] + sigma[6] <= 12
 passenger_delivery5,7: 11 vars[5,7] - sigma[5] + sigma[7] <= 12
 passenger_delivery5,8: 9 vars[5,8] - sigma[5] + sigma[8] <= 12
 passenger_delivery5,9: 12 vars[5,9] - sigma[5] + sigma[9] <= 12
 passenger_delivery5,10: 10 vars[5,10] - sigma[5] + sigma[10] <= 12
 passenger_delivery6,1: 7 vars[6,1] + sigma[1] - sigma[6] <= 12
 passenger_delivery6,2: 6 vars[6,2] + sigma[2] - sigma[6] <= 12
 passenger_delivery6,3: 6 vars[6,3] + sigma[3] - sigma[6] <= 12
 passenger_delivery6,4: 9 vars[6,4] + sigma[4] - sigma[6] <= 12
 passenger_delivery6,5: 6 vars[6,5] + sigma[5] - sigma[6] <= 12
 passenger_delivery6,7: 11 vars[6,7] - sigma[6] + sigma[7] <= 12
 passenger_delivery6,8: 9 vars[6,8] - sigma[6] + sigma[8] <= 12
 passenger_delivery6,9: 12 vars[6,9] - sigma[6] + sigma[9] <= 12
 passenger_delivery6,10: 10 vars[6,10] - sigma[6] + sigma[10] <= 12
 passenger_delivery7,1: 7 vars[7,1] + sigma[1] - sigma[7] <= 12
 passenger_delivery7,2: 6 vars[7,2] + sigma[2] - sigma[7] <= 12
 passenger_delivery7,3: 6 vars[7,3] + sigma[3] - sigma[7] <= 12
 passenger_delivery7,4: 9 vars[7,4] + sigma[4] - sigma[7] <= 12
 passenger_delivery7,5: 6 vars[7,5] + sigma[5] - sigma[7] <= 12
 passenger_delivery7,6: 6 vars[7,6] + sigma[6] - sigma[7] <= 12
 passenger_delivery7,8: 9 vars[7,8] - sigma[7] + sigma[8] <= 12
 passenger_delivery7,9: 12 vars[7,9] - sigma[7] + sigma[9] <= 12
 passenger_delivery7,10: 10 vars[7,10] - sigma[7] + sigma[10] <= 12
 passenger_delivery8,1: 7 vars[8,1] + sigma[1] - sigma[8] <= 12
 passenger_delivery8,2: 6 vars[8,2] + sigma[2] - sigma[8] <= 12
 passenger_delivery8,3: 6 vars[8,3] + sigma[3] - sigma[8] <= 12
 passenger_delivery8,4: 9 vars[8,4] + sigma[4] - sigma[8] <= 12
 passenger_delivery8,5: 6 vars[8,5] + sigma[5] - sigma[8] <= 12
 passenger_delivery8,6: 6 vars[8,6] + sigma[6] - sigma[8] <= 12
 passenger_delivery8,7: 11 vars[8,7] + sigma[7] - sigma[8] <= 12
 passenger_delivery8,9: 12 vars[8,9] - sigma[8] + sigma[9] <= 12
 passenger_delivery8,10: 10 vars[8,10] - sigma[8] + sigma[10] <= 12
 passenger_delivery9,1: 7 vars[9,1] + sigma[1] - sigma[9] <= 12
 passenger_delivery9,2: 6 vars[9,2] + sigma[2] - sigma[9] <= 12
 passenger_delivery9,3: 6 vars[9,3] + sigma[3] - sigma[9] <= 12
 passenger_delivery9,4: 9 vars[9,4] + sigma[4] - sigma[9] <= 12
 passenger_delivery9,5: 6 vars[9,5] + sigma[5] - sigma[9] <= 12
 passenger_delivery9,6: 6 vars[9,6] + sigma[6] - sigma[9] <= 12
 passenger_delivery9,7: 11 vars[9,7] + sigma[7] - sigma[9] <= 12
 passenger_delivery9,8: 9 vars[9,8] + sigma[8] - sigma[9] <= 12
 passenger_delivery9,10: 10 vars[9,10] - sigma[9] + sigma[10] <= 12
 passenger_delivery10,1: 7 vars[10,1] + sigma[1] - sigma[10] <= 12
 passenger_delivery10,2: 6 vars[10,2] + sigma[2] - sigma[10] <= 12
 passenger_delivery10,3: 6 vars[10,3] + sigma[3] - sigma[10] <= 12
 passenger_delivery10,4: 9 vars[10,4] + sigma[4] - sigma[10] <= 12
 passenger_delivery10,5: 6 vars[10,5] + sigma[5] - sigma[10] <= 12
 passenger_delivery10,6: 6 vars[10,6] + sigma[6] - sigma[10] <= 12
 passenger_delivery10,7: 11 vars[10,7] + sigma[7] - sigma[10] <= 12
 passenger_delivery10,8: 9 vars[10,8] + sigma[8] - sigma[10] <= 12
 passenger_delivery10,9: 12 vars[10,9] + sigma[9] - sigma[10] <= 12
 picked_up_passengers_limit1: - sigma[1] + pi[1] <= 0
 picked_up_passengers_limit2: - sigma[2] + pi[2] <= 0
 picked_up_passengers_limit3: - sigma[3] + pi[3] <= 0
 picked_up_passengers_limit4: - sigma[4] + pi[4] <= 0
 picked_up_passengers_limit5: - sigma[5] + pi[5] <= 0
 picked_up_passengers_limit6: - sigma[6] + pi[6] <= 0
 picked_up_passengers_limit7: - sigma[7] + pi[7] <= 0
 picked_up_passengers_limit8: - sigma[8] + pi[8] <= 0
 picked_up_passengers_limit9: - sigma[9] + pi[9] <= 0
 picked_up_passengers_limit10: - sigma[10] + pi[10] <= 0
 picked_up_passengers_limit11: - sigma[11] + pi[11] <= 0
 picked_up_cargo_limit1: - c[1] + q[1] <= 0
 picked_up_cargo_limit2: - c[2] + q[2] <= 0
 picked_up_cargo_limit3: - c[3] + q[3] <= 0
 picked_up_cargo_limit4: - c[4] + q[4] <= 0
 picked_up_cargo_limit5: - c[5] + q[5] <= 0
 picked_up_cargo_limit6: - c[6] + q[6] <= 0
 picked_up_cargo_limit7: - c[7] + q[7] <= 0
 picked_up_cargo_limit8: - c[8] + q[8] <= 0
 picked_up_cargo_limit9: - c[9] + q[9] <= 0
 picked_up_cargo_limit10: - c[10] + q[10] <= 0
 picked_up_cargo_limit11: - c[11] + q[11] <= 0
 current_pass0,1: - 7 vars[0,1] - pi[0] + pi[1] >= -6
 current_pass0,2: - 9 vars[0,2] - pi[0] + pi[2] >= -6
 current_pass0,3: - 9 vars[0,3] - pi[0] + pi[3] >= -6
 current_pass0,4: - 11 vars[0,4] - pi[0] + pi[4] >= -6
 current_pass0,5: - 7 vars[0,5] - pi[0] + pi[5] >= -6
 current_pass0,6: - 5 vars[0,6] - pi[0] + pi[6] >= -6
 current_pass0,7: - 3 vars[0,7] - pi[0] + pi[7] >= -6
 current_pass0,8: - 3 vars[0,8] - pi[0] + pi[8] >= -6
 current_pass0,9: - vars[0,9] - pi[0] + pi[9] >= -6
 current_pass0,10: - 5 vars[0,10] - pi[0] + pi[10] >= -6
 current_pass0,11: - 6 vars[0,11] - pi[0] + pi[11] >= -6
 current_pass1,2: - 9 vars[1,2] - pi[1] + pi[2] >= -6
 current_pass1,3: - 9 vars[1,3] - pi[1] + pi[3] >= -6
 current_pass1,4: - 11 vars[1,4] - pi[1] + pi[4] >= -6
 current_pass1,5: - 7 vars[1,5] - pi[1] + pi[5] >= -6
 current_pass1,6: - 5 vars[1,6] - pi[1] + pi[6] >= -6
 current_pass1,7: - 3 vars[1,7] - pi[1] + pi[7] >= -6
 current_pass1,8: - 3 vars[1,8] - pi[1] + pi[8] >= -6
 current_pass1,9: - vars[1,9] - pi[1] + pi[9] >= -6
 current_pass1,10: - 5 vars[1,10] - pi[1] + pi[10] >= -6
 current_pass1,11: - 6 vars[1,11] - pi[1] + pi[11] >= -6
 current_pass2,1: - 7 vars[2,1] + pi[1] - pi[2] >= -6
 current_pass2,3: - 9 vars[2,3] - pi[2] + pi[3] >= -6
 current_pass2,4: - 11 vars[2,4] - pi[2] + pi[4] >= -6
 current_pass2,5: - 7 vars[2,5] - pi[2] + pi[5] >= -6
 current_pass2,6: - 5 vars[2,6] - pi[2] + pi[6] >= -6
 current_pass2,7: - 3 vars[2,7] - pi[2] + pi[7] >= -6
 current_pass2,8: - 3 vars[2,8] - pi[2] + pi[8] >= -6
 current_pass2,9: - vars[2,9] - pi[2] + pi[9] >= -6
 current_pass2,10: - 5 vars[2,10] - pi[2] + pi[10] >= -6
 current_pass2,11: - 6 vars[2,11] - pi[2] + pi[11] >= -6
 current_pass3,1: - 7 vars[3,1] + pi[1] - pi[3] >= -6
 current_pass3,2: - 9 vars[3,2] + pi[2] - pi[3] >= -6
 current_pass3,4: - 11 vars[3,4] - pi[3] + pi[4] >= -6
 current_pass3,5: - 7 vars[3,5] - pi[3] + pi[5] >= -6
 current_pass3,6: - 5 vars[3,6] - pi[3] + pi[6] >= -6
 current_pass3,7: - 3 vars[3,7] - pi[3] + pi[7] >= -6
 current_pass3,8: - 3 vars[3,8] - pi[3] + pi[8] >= -6
 current_pass3,9: - vars[3,9] - pi[3] + pi[9] >= -6
 current_pass3,10: - 5 vars[3,10] - pi[3] + pi[10] >= -6
 current_pass3,11: - 6 vars[3,11] - pi[3] + pi[11] >= -6
 current_pass4,1: - 7 vars[4,1] + pi[1] - pi[4] >= -6
 current_pass4,2: - 9 vars[4,2] + pi[2] - pi[4] >= -6
 current_pass4,3: - 9 vars[4,3] + pi[3] - pi[4] >= -6
 current_pass4,5: - 7 vars[4,5] - pi[4] + pi[5] >= -6
 current_pass4,6: - 5 vars[4,6] - pi[4] + pi[6] >= -6
 current_pass4,7: - 3 vars[4,7] - pi[4] + pi[7] >= -6
 current_pass4,8: - 3 vars[4,8] - pi[4] + pi[8] >= -6
 current_pass4,9: - vars[4,9] - pi[4] + pi[9] >= -6
 current_pass4,10: - 5 vars[4,10] - pi[4] + pi[10] >= -6
 current_pass4,11: - 6 vars[4,11] - pi[4] + pi[11] >= -6
 current_pass5,1: - 7 vars[5,1] + pi[1] - pi[5] >= -6
 current_pass5,2: - 9 vars[5,2] + pi[2] - pi[5] >= -6
 current_pass5,3: - 9 vars[5,3] + pi[3] - pi[5] >= -6
 current_pass5,4: - 11 vars[5,4] + pi[4] - pi[5] >= -6
 current_pass5,6: - 5 vars[5,6] - pi[5] + pi[6] >= -6
 current_pass5,7: - 3 vars[5,7] - pi[5] + pi[7] >= -6
 current_pass5,8: - 3 vars[5,8] - pi[5] + pi[8] >= -6
 current_pass5,9: - vars[5,9] - pi[5] + pi[9] >= -6
 current_pass5,10: - 5 vars[5,10] - pi[5] + pi[10] >= -6
 current_pass5,11: - 6 vars[5,11] - pi[5] + pi[11] >= -6
 current_pass6,1: - 7 vars[6,1] + pi[1] - pi[6] >= -6
 current_pass6,2: - 9 vars[6,2] + pi[2] - pi[6] >= -6
 current_pass6,3: - 9 vars[6,3] + pi[3] - pi[6] >= -6
 current_pass6,4: - 11 vars[6,4] + pi[4] - pi[6] >= -6
 current_pass6,5: - 7 vars[6,5] + pi[5] - pi[6] >= -6
 current_pass6,7: - 3 vars[6,7] - pi[6] + pi[7] >= -6
 current_pass6,8: - 3 vars[6,8] - pi[6] + pi[8] >= -6
 current_pass6,9: - vars[6,9] - pi[6] + pi[9] >= -6
 current_pass6,10: - 5 vars[6,10] - pi[6] + pi[10] >= -6
 current_pass6,11: - 6 vars[6,11] - pi[6] + pi[11] >= -6
 current_pass7,1: - 7 vars[7,1] + pi[1] - pi[7] >= -6
 current_pass7,2: - 9 vars[7,2] + pi[2] - pi[7] >= -6
 current_pass7,3: - 9 vars[7,3] + pi[3] - pi[7] >= -6
 current_pass7,4: - 11 vars[7,4] + pi[4] - pi[7] >= -6
 current_pass7,5: - 7 vars[7,5] + pi[5] - pi[7] >= -6
 current_pass7,6: - 5 vars[7,6] + pi[6] - pi[7] >= -6
 current_pass7,8: - 3 vars[7,8] - pi[7] + pi[8] >= -6
 current_pass7,9: - vars[7,9] - pi[7] + pi[9] >= -6
 current_pass7,10: - 5 vars[7,10] - pi[7] + pi[10] >= -6
 current_pass7,11: - 6 vars[7,11] - pi[7] + pi[11] >= -6
 current_pass8,1: - 7 vars[8,1] + pi[1] - pi[8] >= -6
 current_pass8,2: - 9 vars[8,2] + pi[2] - pi[8] >= -6
 current_pass8,3: - 9 vars[8,3] + pi[3] - pi[8] >= -6
 current_pass8,4: - 11 vars[8,4] + pi[4] - pi[8] >= -6
 current_pass8,5: - 7 vars[8,5] + pi[5] - pi[8] >= -6
 current_pass8,6: - 5 vars[8,6] + pi[6] - pi[8] >= -6
 current_pass8,7: - 3 vars[8,7] + pi[7] - pi[8] >= -6
 current_pass8,9: - vars[8,9] - pi[8] + pi[9] >= -6
 current_pass8,10: - 5 vars[8,10] - pi[8] + pi[10] >= -6
 current_pass8,11: - 6 vars[8,11] - pi[8] + pi[11] >= -6
 current_pass9,1: - 7 vars[9,1] + pi[1] - pi[9] >= -6
 current_pass9,2: - 9 vars[9,2] + pi[2] - pi[9] >= -6
 current_pass9,3: - 9 vars[9,3] + pi[3] - pi[9] >= -6
 current_pass9,4: - 11 vars[9,4] + pi[4] - pi[9] >= -6
 current_pass9,5: - 7 vars[9,5] + pi[5] - pi[9] >= -6
 current_pass9,6: - 5 vars[9,6] + pi[6] - pi[9] >= -6
 current_pass9,7: - 3 vars[9,7] + pi[7] - pi[9] >= -6
 current_pass9,8: - 3 vars[9,8] + pi[8] - pi[9] >= -6
 current_pass9,10: - 5 vars[9,10] - pi[9] + pi[10] >= -6
 current_pass9,11: - 6 vars[9,11] - pi[9] + pi[11] >= -6
 current_pass10,1: - 7 vars[10,1] + pi[1] - pi[10] >= -6
 current_pass10,2: - 9 vars[10,2] + pi[2] - pi[10] >= -6
 current_pass10,3: - 9 vars[10,3] + pi[3] - pi[10] >= -6
 current_pass10,4: - 11 vars[10,4] + pi[4] - pi[10] >= -6
 current_pass10,5: - 7 vars[10,5] + pi[5] - pi[10] >= -6
 current_pass10,6: - 5 vars[10,6] + pi[6] - pi[10] >= -6
 current_pass10,7: - 3 vars[10,7] + pi[7] - pi[10] >= -6
 current_pass10,8: - 3 vars[10,8] + pi[8] - pi[10] >= -6
 current_pass10,9: - vars[10,9] + pi[9] - pi[10] >= -6
 current_pass10,11: - 6 vars[10,11] - pi[10] + pi[11] >= -6
 current_cargo0,1: - 1200 vars[0,1] - q[0] + q[1] >= -800
 current_cargo0,2: - 900 vars[0,2] - q[0] + q[2] >= -800
 current_cargo0,3: - 800 vars[0,3] - q[0] + q[3] >= -800
 current_cargo0,4: - 1100 vars[0,4] - q[0] + q[4] >= -800
 current_cargo0,5: - 900 vars[0,5] - q[0] + q[5] >= -800
 current_cargo0,6: - 400 vars[0,6] - q[0] + q[6] >= -800
 current_cargo0,7: - 700 vars[0,7] - q[0] + q[7] >= -800
 current_cargo0,8: - 800 vars[0,8] - q[0] + q[8] >= -800
 current_cargo0,9: - 500 vars[0,9] - q[0] + q[9] >= -800
 current_cargo0,10: - 700 vars[0,10] - q[0] + q[10] >= -800
 current_cargo0,11: - 800 vars[0,11] - q[0] + q[11] >= -800
 current_cargo1,2: - 900 vars[1,2] - q[1] + q[2] >= -800
 current_cargo1,3: - 800 vars[1,3] - q[1] + q[3] >= -800
 current_cargo1,4: - 1100 vars[1,4] - q[1] + q[4] >= -800
 current_cargo1,5: - 900 vars[1,5] - q[1] + q[5] >= -800
 current_cargo1,6: - 400 vars[1,6] - q[1] + q[6] >= -800
 current_cargo1,7: - 700 vars[1,7] - q[1] + q[7] >= -800
 current_cargo1,8: - 800 vars[1,8] - q[1] + q[8] >= -800
 current_cargo1,9: - 500 vars[1,9] - q[1] + q[9] >= -800
 current_cargo1,10: - 700 vars[1,10] - q[1] + q[10] >= -800
 current_cargo1,11: - 800 vars[1,11] - q[1] + q[11] >= -800
 current_cargo2,1: - 1200 vars[2,1] + q[1] - q[2] >= -800
 current_cargo2,3: - 800 vars[2,3] - q[2] + q[3] >= -800
 current_cargo2,4: - 1100 vars[2,4] - q[2] + q[4] >= -800
 current_cargo2,5: - 900 vars[2,5] - q[2] + q[5] >= -800
 current_cargo2,6: - 400 vars[2,6] - q[2] + q[6] >= -800
 current_cargo2,7: - 700 vars[2,7] - q[2] + q[7] >= -800
 current_cargo2,8: - 800 vars[2,8] - q[2] + q[8] >= -800
 current_cargo2,9: - 500 vars[2,9] - q[2] + q[9] >= -800
 current_cargo2,10: - 700 vars[2,10] - q[2] + q[10] >= -800
 current_cargo2,11: - 800 vars[2,11] - q[2] + q[11] >= -800
 current_cargo3,1: - 1200 vars[3,1] + q[1] - q[3] >= -800
 current_cargo3,2: - 900 vars[3,2] + q[2] - q[3] >= -800
 current_cargo3,4: - 1100 vars[3,4] - q[3] + q[4] >= -800
 current_cargo3,5: - 900 vars[3,5] - q[3] + q[5] >= -800
 current_cargo3,6: - 400 vars[3,6] - q[3] + q[6] >= -800
 current_cargo3,7: - 700 vars[3,7] - q[3] + q[7] >= -800
 current_cargo3,8: - 800 vars[3,8] - q[3] + q[8] >= -800
 current_cargo3,9: - 500 vars[3,9] - q[3] + q[9] >= -800
 current_cargo3,10: - 700 vars[3,10] - q[3] + q[10] >= -800
 current_cargo3,11: - 800 vars[3,11] - q[3] + q[11] >= -800
 current_cargo4,1: - 1200 vars[4,1] + q[1] - q[4] >= -800
 current_cargo4,2: - 900 vars[4,2] + q[2] - q[4] >= -800
 current_cargo4,3: - 800 vars[4,3] + q[3] - q[4] >= -800
 current_cargo4,5: - 900 vars[4,5] - q[4] + q[5] >= -800
 current_cargo4,6: - 400 vars[4,6] - q[4] + q[6] >= -800
 current_cargo4,7: - 700 vars[4,7] - q[4] + q[7] >= -800
 current_cargo4,8: - 800 vars[4,8] - q[4] + q[8] >= -800
 current_cargo4,9: - 500 vars[4,9] - q[4] + q[9] >= -800
 current_cargo4,10: - 700 vars[4,10] - q[4] + q[10] >= -800
 current_cargo4,11: - 800 vars[4,11] - q[4] + q[11] >= -800
 current_cargo5,1: - 1200 vars[5,1] + q[1] - q[5] >= -800
 current_cargo5,2: - 900 vars[5,2] + q[2] - q[5] >= -800
 current_cargo5,3: - 800 vars[5,3] + q[3] - q[5] >= -800
 current_cargo5,4: - 1100 vars[5,4] + q[4] - q[5] >= -800
 current_cargo5,6: - 400 vars[5,6] - q[5] + q[6] >= -800
 current_cargo5,7: - 700 vars[5,7] - q[5] + q[7] >= -800
 current_cargo5,8: - 800 vars[5,8] - q[5] + q[8] >= -800
 current_cargo5,9: - 500 vars[5,9] - q[5] + q[9] >= -800
 current_cargo5,10: - 700 vars[5,10] - q[5] + q[10] >= -800
 current_cargo5,11: - 800 vars[5,11] - q[5] + q[11] >= -800
 current_cargo6,1: - 1200 vars[6,1] + q[1] - q[6] >= -800
 current_cargo6,2: - 900 vars[6,2] + q[2] - q[6] >= -800
 current_cargo6,3: - 800 vars[6,3] + q[3] - q[6] >= -800
 current_cargo6,4: - 1100 vars[6,4] + q[4] - q[6] >= -800
 current_cargo6,5: - 900 vars[6,5] + q[5] - q[6] >= -800
 current_cargo6,7: - 700 vars[6,7] - q[6] + q[7] >= -800
 current_cargo6,8: - 800 vars[6,8] - q[6] + q[8] >= -800
 current_cargo6,9: - 500 vars[6,9] - q[6] + q[9] >= -800
 current_cargo6,10: - 700 vars[6,10] - q[6] + q[10] >= -800
 current_cargo6,11: - 800 vars[6,11] - q[6] + q[11] >= -800
 current_cargo7,1: - 1200 vars[7,1] + q[1] - q[7] >= -800
 current_cargo7,2: - 900 vars[7,2] + q[2] - q[7] >= -800
 current_cargo7,3: - 800 vars[7,3] + q[3] - q[7] >= -800
 current_cargo7,4: - 1100 vars[7,4] + q[4] - q[7] >= -800
 current_cargo7,5: - 900 vars[7,5] + q[5] - q[7] >= -800
 current_cargo7,6: - 400 vars[7,6] + q[6] - q[7] >= -800
 current_cargo7,8: - 800 vars[7,8] - q[7] + q[8] >= -800
 current_cargo7,9: - 500 vars[7,9] - q[7] + q[9] >= -800
 current_cargo7,10: - 700 vars[7,10] - q[7] + q[10] >= -800
 current_cargo7,11: - 800 vars[7,11] - q[7] + q[11] >= -800
 current_cargo8,1: - 1200 vars[8,1] + q[1] - q[8] >= -800
 current_cargo8,2: - 900 vars[8,2] + q[2] - q[8] >= -800
 current_cargo8,3: - 800 vars[8,3] + q[3] - q[8] >= -800
 current_cargo8,4: - 1100 vars[8,4] + q[4] - q[8] >= -800
 current_cargo8,5: - 900 vars[8,5] + q[5] - q[8] >= -800
 current_cargo8,6: - 400 vars[8,6] + q[6] - q[8] >= -800
 current_cargo8,7: - 700 vars[8,7] + q[7] - q[8] >= -800
 current_cargo8,9: - 500 vars[8,9] - q[8] + q[9] >= -800
 current_cargo8,10: - 700 vars[8,10] - q[8] + q[10] >= -800
 current_cargo8,11: - 800 vars[8,11] - q[8] + q[11] >= -800
 current_cargo9,1: - 1200 vars[9,1] + q[1] - q[9] >= -800
 current_cargo9,2: - 900 vars[9,2] + q[2] - q[9] >= -800
 current_cargo9,3: - 800 vars[9,3] + q[3] - q[9] >= -800
 current_cargo9,4: - 1100 vars[9,4] + q[4] - q[9] >= -800
 current_cargo9,5: - 900 vars[9,5] + q[5] - q[9] >= -800
 current_cargo9,6: - 400 vars[9,6] + q[6] - q[9] >= -800
 current_cargo9,7: - 700 vars[9,7] + q[7] - q[9] >= -800
 current_cargo9,8: - 800 vars[9,8] + q[8] - q[9] >= -800
 current_cargo9,10: - 700 vars[9,10] - q[9] + q[10] >= -800
 current_cargo9,11: - 800 vars[9,11] - q[9] + q[11] >= -800
 current_cargo10,1: - 1200 vars[10,1] + q[1] - q[10] >= -800
 current_cargo10,2: - 900 vars[10,2] + q[2] - q[10] >= -800
 current_cargo10,3: - 800 vars[10,3] + q[3] - q[10] >= -800
 current_cargo10,4: - 1100 vars[10,4] + q[4] - q[10] >= -800
 current_cargo10,5: - 900 vars[10,5] + q[5] - q[10] >= -800
 current_cargo10,6: - 400 vars[10,6] + q[6] - q[10] >= -800
 current_cargo10,7: - 700 vars[10,7] + q[7] - q[10] >= -800
 current_cargo10,8: - 800 vars[10,8] + q[8] - q[10] >= -800
 current_cargo10,9: - 500 vars[10,9] + q[9] - q[10] >= -800
 current_cargo10,11: - 800 vars[10,11] - q[10] + q[11] >= -800
Bounds
 sigma[0] <= 6
 sigma[1] <= 6
 sigma[2] <= 6
 sigma[3] <= 6
 sigma[4] <= 6
 sigma[5] <= 6
 sigma[6] <= 6
 sigma[7] <= 6
 sigma[8] <= 6
 sigma[9] <= 6
 sigma[10] <= 6
 sigma[11] <= 6
 c[0] <= 800
 c[1] <= 800
 c[2] <= 800
 c[3] <= 800
 c[4] <= 800
 c[5] <= 800
 c[6] <= 800
 c[7] <= 800
 c[8] <= 800
 c[9] <= 800
 c[10] <= 800
 c[11] <= 800
 pi[0] <= 6
 pi[1] <= 6
 pi[2] <= 6
 pi[3] <= 6
 pi[4] <= 6
 pi[5] <= 6
 pi[6] <= 6
 pi[7] <= 6
 pi[8] <= 6
 pi[9] <= 6
 pi[10] <= 6
 pi[11] <= 6
 q[0] <= 800
 q[1] <= 800
 q[2] <= 800
 q[3] <= 800
 q[4] <= 800
 q[5] <= 800
 q[6] <= 800
 q[7] <= 800
 q[8] <= 800
 q[9] <= 800
 q[10] <= 800
 q[11] <= 800
Binaries
 vars[0,1] vars[0,2] vars[0,3] vars[0,4] vars[0,5] vars[0,6] vars[0,7]
 vars[0,8] vars[0,9] vars[0,10] vars[0,11] vars[1,0] vars[1,2] vars[1,3]
 vars[1,4] vars[1,5] vars[1,6] vars[1,7] vars[1,8] vars[1,9] vars[1,10]
 vars[1,11] vars[2,0] vars[2,1] vars[2,3] vars[2,4] vars[2,5] vars[2,6]
 vars[2,7] vars[2,8] vars[2,9] vars[2,10] vars[2,11] vars[3,0] vars[3,1]
 vars[3,2] vars[3,4] vars[3,5] vars[3,6] vars[3,7] vars[3,8] vars[3,9]
 vars[3,10] vars[3,11] vars[4,0] vars[4,1] vars[4,2] vars[4,3] vars[4,5]
 vars[4,6] vars[4,7] vars[4,8] vars[4,9] vars[4,10] vars[4,11] vars[5,0]
 vars[5,1] vars[5,2] vars[5,3] vars[5,4] vars[5,6] vars[5,7] vars[5,8]
 vars[5,9] vars[5,10] vars[5,11] vars[6,0] vars[6,1] vars[6,2] vars[6,3]
 vars[6,4] vars[6,5] vars[6,7] vars[6,8] vars[6,9] vars[6,10] vars[6,11]
 vars[7,0] vars[7,1] vars[7,2] vars[7,3] vars[7,4] vars[7,5] vars[7,6]
 vars[7,8] vars[7,9] vars[7,10] vars[7,11] vars[8,0] vars[8,1] vars[8,2]
 vars[8,3] vars[8,4] vars[8,5] vars[8,6] vars[8,7] vars[8,9] vars[8,10]
 vars[8,11] vars[9,0] vars[9,1] vars[9,2] vars[9,3] vars[9,4] vars[9,5]
 vars[9,6] vars[9,7] vars[9,8] vars[9,10] vars[9,11] vars[10,0] vars[10,1]
 vars[10,2] vars[10,3] vars[10,4] vars[10,5] vars[10,6] vars[10,7]
 vars[10,8] vars[10,9] vars[10,11] vars[11,0] vars[11,1] vars[11,2]
 vars[11,3] vars[11,4] vars[11,5] vars[11,6] vars[11,7] vars[11,8]
 vars[11,9] vars[11,10]
End
