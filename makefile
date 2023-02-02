PROJECTS := bare full library

define build_project
	cookiecutter https://github.com/tedivm/tedivms_awesome_python_template --config-file confs/$(1).yaml --no-input
endef

all: $(PROJECTS)

bare:
	$(call build_project,bare)

full:
	$(call build_project,full)

library:
	$(call build_project,library)


rebuild_all: $(addprefix rebuild_,$(PROJECTS))

rebuild_bare:
	rm -Rf bare
	$(call build_project,bare)

rebuild_full:
	rm -Rf full
	$(call build_project,full)

rebuild_library:
	rm -Rf library
	$(call build_project,library)
