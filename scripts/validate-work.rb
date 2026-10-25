require 'yaml'
require 'set'

root = File.expand_path('..', __dir__)
build = File.expand_path(ARGV[0] || '_site', root)
records = Dir["#{root}/content/_work/*.md"].map do |path|
  _, yaml, body = File.read(path).split(/^---\s*$\n?/, 3)
  data = YAML.safe_load(yaml)
  %w[key title type tags permalink order featured].each do |field|
    raise "#{path}: missing #{field}" unless data.key?(field)
  end
  raise "#{path}: invalid type" unless %w[project research artwork].include?(data['type'])
  raise "#{path}: tags must be a list" unless data['tags'].is_a?(Array)
  raise "#{path}: invalid featured flag" unless [true, false].include?(data['featured'])
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
raise 'Work must list every entry exactly once' unless shown.size == keys.size && shown.to_set == keys
puts "Validated #{records.size} work records, parents, unique URLs and the complete Work index."
