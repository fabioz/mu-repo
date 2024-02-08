#!/usr/bin/env python
if __name__ == '__main__':
    import sys
    import mu_repo

    status = mu_repo.main()
    success = status is None or status.succeeded
    sys.exit(0 if success else 1)
