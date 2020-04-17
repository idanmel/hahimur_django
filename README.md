# Hahimur-Django
Backend for Hahimur, which is a site for my friends and I to predict
major football tournament games.

## Authorization
Every User has a token, and should be passed as a query parameter
```bash
https://live-site.com/tournaments/1/predictions?token=<token>
```

## API Endpoints
```bash
POST    '/tournaments/<int>/predictions'
```


#### POST '/tournaments'
The post request should have a json body containing all the group matches, 
knockout matches and top_scorer.
like so:
```json
{
   "group_matches": [
      { 
        "match_number": Int, 
        "home_score": Int, 
        "away_score": Int
      }
  ],
  "knockout_matches": [
      { 
        "match_number": Int, 
        "home_score": Int, 
        "away_score": Int,
        "home_win": Boolean
      }
  ],
  "top_scorer": String
 
}
```