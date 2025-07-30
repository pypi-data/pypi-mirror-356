from fyg import Config, PCache

config = Config({
	"html": True,
	"scantick": 2,
	"verbose": True,
	"gmailer": False,
	"cache": PCache(".cm"),
	"admin": {
		"contacts": [],
		"reportees": []
	}
})