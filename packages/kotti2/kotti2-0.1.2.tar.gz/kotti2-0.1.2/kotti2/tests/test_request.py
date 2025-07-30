class TestExtendingRequest:
    def test_it(self):
        from kotti2.request import Request
        from zope.interface import providedBy, implementedBy

        req = Request({})
        req.set_property(lambda x: "exists", "marker", reify=True)

        assert providedBy(req) == implementedBy(Request)
        assert req.marker == "exists"
