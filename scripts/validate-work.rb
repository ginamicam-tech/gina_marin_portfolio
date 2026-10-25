require 'yaml'
require 'set'

root = File.expand_path('..', __dir__)
build = File.expand_path(ARGV[0] || '_site', root)
records = Dir["#{root}/content/_work/*.md"].map do |path|
  _, yaml, body = File.read(path).split(/^---\s*$\n?/, 3)
  data = YAML.safe_load(yaml)
  %w[key title type tags permalink order featured card_label year].each do |field|
    raise "#{path}: missing #{field}" unless data.key?(field)
  end
  raise "#{path}: invalid type" unless %w[project research artwork series].include?(data['type'])
  raise "#{path}: tags must be a list" unless data['tags'].is_a?(Array)
  raise "#{path}: invalid featured flag" unless [true, false].include?(data['featured'])
  raise "#{path}: card_label must be nonempty text" unless data['card_label'].is_a?(String) && !data['card_label'].strip.empty?
  raise "#{path}: year must be numeric" unless data['year'].is_a?(Integer)
  if data['year_start']
    raise "#{path}: invalid year range" unless data['year_start'].is_a?(Integer) && data['year_start'] <= data['year']
  end
  if data['type'] == 'artwork'
    %w[series year technique dimensions cover].each { |field| raise "#{path}: missing #{field}" unless data[field] }
  end
  data
end
%w[key permalink].each do |field|
  values = records.map { |r| r[field] }
  raise "Duplicate #{field}" unless values.uniq.size == values.size
end
keys = records.map { |r| r['key'] }.to_set
records.each do |r|
  raise "Unknown parent #{r['parent']}" if r['parent'] && !keys.include?(r['parent'])
  raise "Missing page #{r['permalink']}" unless File.file?(File.join(build, r['permalink'].sub(%r{^/}, ''), 'index.html'))
end
shown = File.read(File.join(build, 'work/index.html')).scan(/data-work-id="([^"]+)"/).flatten
index_keys = records.reject { |r| r['type'] == 'artwork' }.map { |r| r['key'] }.to_set
raise 'Work must list projects, research and series exactly once' unless shown.size == index_keys.size && shown.to_set == index_keys
series_records = records.select { |r| r['type'] == 'series' }
covered = []
series_records.each do |r|
  selection = r.fetch('work_lists').first
  expected = records.select { |a| a['type'] == 'artwork' && a['series'] == selection['series'] }
  raise "Empty artwork series #{r['key']}" if expected.empty?
  html = File.read(File.join(build, r['permalink'].sub(%r{^/}, ''), 'index.html'))
  gallery_keys = html.scan(/data-work-id="([^"]+)"/).flatten
  expected_keys = expected.map { |a| a['key'] }
  raise "Incomplete series gallery #{r['key']}" unless gallery_keys.size == expected_keys.size && gallery_keys.to_set == expected_keys.to_set
  years = gallery_keys.map { |key| expected.find { |a| a['key'] == key }['year'] }
  raise "Series not newest first: #{r['key']}" unless years == years.sort.reverse
  covered.concat(gallery_keys)
end
artwork_keys = records.select { |r| r['type'] == 'artwork' }.map { |r| r['key'] }
raise 'Each artwork must belong to exactly one series gallery' unless covered.sort == artwork_keys.sort
index_years = shown.map { |key| records.find { |r| r['key'] == key }.fetch('year') }
raise 'Work index not newest first' unless index_years == index_years.sort.reverse
puts "Validated #{records.size} work records, parents, unique URLs and the grouped Work index (#{shown.size} cards, #{covered.size} artworks in series)."
