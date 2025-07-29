def generate_group_project_query(full_path, after):
    return {
        'query': """
        query {
            group(fullPath:\"%s\") {
                    projects(after:\"%s\", includeSubgroups:true) {
                    nodes {
                        id,
                        name,
                        fullPath,
                        archived,
                        lastActivityAt,
                        webUrl,
                        namespace {
                            fullPath
                        }
                        statistics {
                            packagesSize,
                            containerRegistrySize,
                            repositorySize,
                            wikiSize,
                            lfsObjectsSize,
                            snippetsSize,
                            uploadsSize,
                            commitCount,
                            buildArtifactsSize,
                            storageSize
                        }
                        packages {
                            nodes {
                                packageType
                            }
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """ % (full_path, after)
    }


def generate_all_projects_query(after):
    return {
        'query': """
            query {
                projects(after:\"%s\") {
                    nodes {
                        id,
                        name,
                        fullPath,
                        archived,
                        lastActivityAt,
                        webUrl,
                        namespace {
                            fullPath
                        }
                        statistics {
                            packagesSize,
                            containerRegistrySize,
                            repositorySize,
                            wikiSize,
                            lfsObjectsSize,
                            snippetsSize,
                            uploadsSize,
                            commitCount,
                            buildArtifactsSize,
                            storageSize
                        }
                        packages {
                            nodes {
                                packageType
                            }
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
            """ % after
    }
